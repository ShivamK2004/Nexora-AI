# Nexora AI — Multi-Model AI Assistant Platform


Nexora AI is a multi-model AI assistant platform designed to bring different AI providers into one unified workspace. It provides a ChatGPT-style conversational interface with document analysis, image understanding, persistent chat history, and model selection.

Users can switch between Google Gemini, Anthropic Claude, and Ollama through a unified interface.

Nexora AI is also the foundation for **NexoraLM**, a long-term research initiative focused on developing an independently trained language model instead of permanently depending on third-party AI providers.

> **Project Status:** Nexora AI is an application and model-development starter. Gemini, Claude, and Ollama are currently used as external AI providers. NexoraLM is an experimental research prototype, not yet a production-ready foundation model.

---

## Key Features

### 1. Multi-Model AI Integration

Use multiple AI providers through one application.

- **Google Gemini** — Cloud-based AI conversations and document/image understanding.
- **Anthropic Claude** — Claude-powered conversations and document analysis.
- **Ollama** — Run supported open-weight models using a local or remote Ollama server.
- **Mock Provider** — Test the application without calling an AI model.

Nexora provides separate AI Provider and Model selectors.

### 2. Supported Gemini Models

Nexora AI currently lists these two Gemini models:

| Model | Model ID |
|---|---|
| Gemini 3.8 Flash | `gemini-3.8-flash` |
| Gemini 3.5 Flash Lite | `gemini-3.5-flash-lite` |

Only these two Gemini models are currently included in the Nexora configuration.

### 3. ChatGPT-Style Interface

- Responsive conversational interface.
- Create new conversations.
- Search previous conversations.
- Reopen and delete chat history.
- Persistent conversation storage using SQLite.
- Provider and model selection.
- Browser-based model preferences.
- Conversation-specific file attachments.

### 4. File and Image Uploads

Upload up to five files per message.

Supported formats:

- PDF
- TXT
- Markdown
- CSV
- JSON
- Python
- SQL
- PNG
- JPG / JPEG
- WEBP
- GIF

Additional functionality:

- Drag-and-drop uploads.
- Clipboard image paste.
- Image previews.
- PDF text extraction.
- Document-based question answering.
- Image understanding with compatible AI models.

**Note:** Scanned PDFs without selectable text require OCR before their contents can be analyzed. Image understanding depends on the selected provider and model.

### 5. Knowledge and Memory

- Local knowledge-base storage.
- Document retrieval.
- Conversation history.
- Explicit user-managed memory.
- Bounded agent workflows.
- Persistent application data.

### 6. NexoraLM Research

Nexora includes an experimental language-model development starter.

The long-term objective is to build an independent language model with:

- Custom tokenizer.
- Decoder-only Transformer architecture.
- Pretraining pipeline.
- Training checkpoints.
- Model evaluation.
- Independent inference engine.
- Future instruction tuning.

The experimental implementation is separate from Gemini, Claude, and Ollama integrations.

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| AI Providers | Gemini, Claude, Ollama |
| API Communication | HTTP / REST |
| Model Research | PyTorch |
| Deployment | Docker, Render |
| Version Control | Git, GitHub |

---

## Project Structure

```text
Nexora-AI/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── routers/
│       │   └── chat.py
│       └── services/
│           ├── llm.py
│           └── models.py
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
├── model/
│   └── nexora_lm/
│
├── data/
├── knowledge_base/
├── workspace/
├── docs/
├── tests/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
├── start_windows.bat
└── README.md
```

---

## Installation — Windows

### Prerequisites

- Python 3.10 or newer.
- Git.
- Internet connection for cloud AI providers.
- Ollama, if using local models.

### 1. Clone the repository

```powershell
git clone https://github.com/ShivamK2004/Nexora-AI.git

cd Nexora-AI
```

### 2. Create the environment file

```powershell
Copy-Item .env.example .env
```

### 3. Configure API keys

Open `.env`:

```powershell
notepad .env
```

Configure your providers:

```dotenv
APP_NAME=Nexora AI
APP_ENV=development

LLM_PROVIDER=gemini

# Google Gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.8-flash

# Anthropic Claude
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
ANTHROPIC_MODEL=YOUR_AVAILABLE_CLAUDE_MODEL_ID

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest
OLLAMA_TIMEOUT_SECONDS=120
```

Never commit real API keys to GitHub.

### 4. Start Nexora AI

```powershell
.\start_windows.bat
```

Alternatively, install dependencies manually:

```powershell
py -3.13 -m venv .venv

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

### 5. Open the application

Visit:

http://127.0.0.1:8000

---

## AI Provider Configuration

Nexora provides separate selectors in the chat interface:

- **AI Provider:** Choose Gemini, Anthropic Claude, Ollama, or Mock.
- **Model:** Select a model supported by the selected provider.

The selected provider and model are sent with each chat request and saved in browser preferences.

### Google Gemini

Currently supported models:

| Model | Model ID |
|---|---|
| Gemini 3.8 Flash | `gemini-3.8-flash` |
| Gemini 3.5 Flash Lite | `gemini-3.5-flash-lite` |

Configuration:

```dotenv
LLM_PROVIDER=gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.8-flash
```

Get your API key:

https://aistudio.google.com/app/apikey

### Anthropic Claude

Claude is available as a separate AI provider.

Configuration:

```dotenv
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
ANTHROPIC_MODEL=YOUR_AVAILABLE_CLAUDE_MODEL_ID
```

Get your API key:

https://console.anthropic.com/

Model availability depends on your Anthropic account and API access. Check the official model catalog before selecting a model.

### Ollama

Install Ollama:

https://ollama.com/

Download a model:

```powershell
ollama pull llama3:latest
```

Configure:

```dotenv
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest
OLLAMA_TIMEOUT_SECONDS=120
```

For image understanding, select a vision-capable model, such as:

```powershell
ollama pull llama3.2-vision
```

Then update `OLLAMA_MODEL` accordingly.

**Important:** Ollama running on your Windows computer is not automatically accessible to a cloud deployment. A remotely deployed Nexora backend requires a separately hosted and securely accessible Ollama server.

### Mock Provider

```dotenv
LLM_PROVIDER=mock
```

Mock mode is for interface and workflow testing. It does not generate genuine AI responses.

---

## Deployment — Render

Nexora AI can be deployed using Docker on Render.

### Deployment Steps

1. Push the project to GitHub.
2. Open https://render.com/.
3. Create a new Web Service.
4. Connect the Nexora AI GitHub repository.
5. Select Docker as the runtime.
6. Configure the required environment variables.
7. Deploy the application.

### Production Environment Variables

```dotenv
APP_ENV=production
LLM_PROVIDER=gemini

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.8-flash
```

Add the Claude API key separately if you want to use Claude.

### Production Considerations

- Configure persistent storage for SQLite and uploaded files.
- Protect API routes with authentication.
- Use HTTPS.
- Configure upload size limits.
- Monitor application logs.
- Secure remote Ollama connections.
- Back up persistent data.

Never store API keys in frontend JavaScript or commit them to GitHub.

---

## Running Tests

Run the test suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover application workflows and mocked provider integrations. Live provider functionality must also be tested with valid API credentials.

---

## Development Roadmap

| Phase | Planned Development |
|---|---|
| Phase 1 | Multi-provider AI assistant |
| Phase 2 | Chat history, document and image analysis |
| Phase 3 | Improved memory and knowledge retrieval |
| Phase 4 | Agent workflows and tool integration |
| Phase 5 | Custom tokenizer and Transformer improvements |
| Phase 6 | NexoraLM pretraining and evaluation |
| Phase 7 | Independent NexoraLM inference and deployment |
| Phase 8 | Voice, vision and multimodal capabilities |

---

## Vision

The long-term vision of Nexora AI is to create an independent AI ecosystem with its own language model, inference engine, memory system, and developer platform.

External AI providers are useful during the initial development and testing stages. However, the ultimate objective is to develop and operate NexoraLM independently.

**Nexora AI — One Platform. Multiple Models. An Independent AI Future.**

---

## License

MIT License.

Review third-party software, model, and dataset licenses independently before redistribution.
