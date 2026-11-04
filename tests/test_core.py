import unittest
from backend.app.services.tools import safe_calculate
from backend.app.services.knowledge import chunk_text
from model.nexora_lm.tokenizer import ByteTokenizer

class CoreTests(unittest.TestCase):
    def test_calculator(self):
        self.assertEqual(safe_calculate('2 + 3 * 4'),14)
        self.assertEqual(safe_calculate('(10 - 4) / 2'),3)
    def test_calculator_rejects_code(self):
        with self.assertRaises(ValueError): safe_calculate('__import__("os").system("whoami")')
    def test_chunking(self):
        chunks=chunk_text('word '*1000,chunk_size=100,overlap=10)
        self.assertGreater(len(chunks),1)
        self.assertTrue(all(chunks))
    def test_byte_tokenizer_round_trip(self):
        value='Nexora AI — नमस्ते'
        tok=ByteTokenizer()
        self.assertEqual(tok.decode(tok.encode(value)),value)

if __name__=='__main__': unittest.main()
