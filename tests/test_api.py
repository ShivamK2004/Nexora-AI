import os, tempfile, unittest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app.config import get_settings
from backend.app.main import app

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Tests are intentionally isolated from any real user data.
        cls.temp=tempfile.TemporaryDirectory()
        os.environ['NEXORA_DATA_DIR']=cls.temp.name
        os.environ['NEXORA_LLM_PROVIDER']='mock'
        get_settings.cache_clear()
        from backend.app.db import init_db
        init_db()
        cls.client=TestClient(app)
    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
        get_settings.cache_clear()
    def test_health(self):
        response=self.client.get('/api/health')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['status'],'ok')

    def test_provider_can_be_switched_from_frontend_and_saved(self):
        from unittest.mock import patch
        from backend.app import main as main_module
        from backend.app.config import get_settings
        with tempfile.TemporaryDirectory() as env_dir:
            env_path = Path(env_dir) / '.env'
            env_path.write_text('LLM_PROVIDER=mock\nGEMINI_API_KEY=test-key\n', encoding='utf-8')
            with patch.dict(os.environ, {'NEXORA_LLM_PROVIDER': 'mock', 'GEMINI_API_KEY': 'test-key'}):
                with patch.object(main_module, '_env_file_path', return_value=env_path):
                    response = self.client.post('/api/provider', json={'provider': 'gemini'})
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()['provider'], 'gemini')
                    self.assertTrue(response.json()['provider_configured'])
                    self.assertIn('LLM_PROVIDER=gemini', env_path.read_text(encoding='utf-8'))
            get_settings.cache_clear()

    def test_provider_switch_rejects_unknown_provider(self):
        response = self.client.post('/api/provider', json={'provider': 'not-a-provider'})
        self.assertEqual(response.status_code, 400)

    def test_model_catalog_contains_gemini_and_claude_choices(self):
        response = self.client.get('/api/models')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn('anthropic', body['providers'])
        self.assertIn('gemini-2.5-flash', [m['id'] for m in body['catalog']['gemini']])
        self.assertIn('claude-sonnet-5-5', [m['id'] for m in body['catalog']['anthropic']])

    def test_chat_accepts_model_and_provider_selection(self):
        response = self.client.post('/api/chat', json={
            'message': 'Hello Nexora', 'provider': 'mock', 'model': 'mock'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['provider'], 'mock')
        self.assertEqual(response.json()['model'], 'mock')

    def test_chat_mock(self):
        response=self.client.post('/api/chat',json={'message':'Hello Nexora'})
        self.assertEqual(response.status_code,200)
        self.assertIn('MOCK MODE',response.json()['answer'])

    def test_document_upload_and_list(self):
        response = self.client.post(
            '/api/documents',
            files={'file': ('guide.md', b'Nexora knowledge retrieval uses chunks and citations.', 'text/markdown')},
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json()['chunks'], 1)
        listed = self.client.get('/api/documents')
        self.assertEqual(listed.status_code, 200)
        self.assertTrue(any(item['filename'] == 'guide.md' for item in listed.json()))


    def test_chat_image_attachment_and_history(self):
        # A small opaque PNG payload is enough to exercise local persistence/routing.
        image_bytes = b"\x89PNG\r\n\x1a\nNEXORA-TEST-IMAGE"
        response = self.client.post(
            '/api/chat',
            data={'message': 'What is in this picture?'},
            files={'files': ('sample.png', image_bytes, 'image/png')},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['attachments'])
        self.assertEqual(body['attachments'][0]['kind'], 'image')
        conversation_id = body['conversation_id']

        detail = self.client.get('/api/conversations/' + conversation_id)
        self.assertEqual(detail.status_code, 200)
        messages = detail.json()['messages']
        self.assertEqual(messages[0]['content'], 'What is in this picture?')
        self.assertEqual(messages[0]['attachments'][0]['filename'], 'sample.png')
        downloaded = self.client.get(messages[0]['attachments'][0]['url'])
        self.assertEqual(downloaded.status_code, 200)
        self.assertEqual(downloaded.content, image_bytes)

        deleted = self.client.delete('/api/conversations/' + conversation_id)
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(self.client.get(messages[0]['attachments'][0]['url']).status_code, 404)

    def test_chat_file_attachment_extracts_text(self):
        response = self.client.post(
            '/api/chat',
            data={'message': 'Summarize this note'},
            files={'files': ('note.txt', b'The Nexora project uses a provider adapter and SQLite.', 'text/plain')},
        )
        self.assertEqual(response.status_code, 200)
        details = self.client.get('/api/conversations/' + response.json()['conversation_id']).json()
        self.assertEqual(details['messages'][0]['content'], 'Summarize this note')
        self.assertEqual(details['messages'][0]['attachments'][0]['filename'], 'note.txt')
        self.assertIn('MOCK MODE', response.json()['answer'])
        self.assertNotIn('provider adapter and SQLite', response.json()['answer'])

    def test_memory_create_and_delete(self):
        created = self.client.post('/api/memories', json={'content': 'Prefers Python examples', 'category': 'preference'})
        self.assertEqual(created.status_code, 200)
        memory_id = created.json()['id']
        self.assertEqual(self.client.get('/api/memories').status_code, 200)
        deleted = self.client.delete('/api/memories/' + memory_id)
        self.assertEqual(deleted.status_code, 200)

    def test_calculator_api(self):
        response=self.client.post('/api/tools/calculate',json={'expression':'6*7'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['result'],42)

if __name__=='__main__':unittest.main()
