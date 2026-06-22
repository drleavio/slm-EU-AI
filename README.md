# EU AI Act Compliance - Custom SLM & API

![EU AI Act](https://img.shields.io/badge/Compliance-EU_AI_Act-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Ollama](https://img.shields.io/badge/Ollama-black?style=flat&logo=ollama)

This project contains a Small Language Model (SLM) based on LLaMA 3.2 1B, fine-tuned/prompted specifically for analyzing **EU AI Act Compliance** risk tiers. It also includes a fully functional FastAPI backend that serves the model locally.

## 🚀 The Model (Hugging Face)

Because the model weights are too large for GitHub, the actual model (`.gguf`) and its `Modelfile` are hosted on Hugging Face.

🔗 **[View and Download the Model on Hugging Face](https://huggingface.co/drlevio/euai-slm)**

## 🧠 How it Works

The API uses a two-step "mixture of models" approach:
1. **Extraction (Groq + LLaMA 3.1):** Uses Groq's blazing-fast inference to extract key facts from the user's AI system description (e.g., intended purpose, domain, risk factors).
2. **Analysis (Local Custom SLM):** Passes the extracted facts to our local custom-trained SLM via Ollama to determine the precise EU AI Act risk tier and rationale.

## 💻 How to Run Locally

If you want to run the backend and the model yourself:

### 1. Set up the Model
1. Install [Ollama](https://ollama.com/).
2. Download the `llama-3.2-1b-instruct.Q4_K_M.gguf` and `Modelfile` from my Hugging Face repository.
3. Open your terminal in the directory where you downloaded them and run:
   ```bash
   ollama create my-trained-slm -f Modelfile
   ```

### 2. Run the FastAPI Backend

#### Using Docker (Recommended)
You can run the entire backend in a Docker container:
```bash
docker build -t slm-backend .
docker run -d -p 8000:8000 -e OLLAMA_HOST="http://host.docker.internal:11434" -e GROQ_API_KEY="your-groq-api-key" slm-backend
```

#### Using Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📚 API Endpoints
- `POST /eu-ai-compliance`: The main endpoint. Pass in `{ "user_input": "description of AI system" }` and receive the extracted facts and risk tier analysis.
- `POST /generate`: Directly prompt the SLM.
- `POST /chat`: Standard chat interface for the SLM.
