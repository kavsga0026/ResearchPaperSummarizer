# Research Paper Summarizer (Backend)

FastAPI server that:
extracts text from PDFs,
detects sections,
summarizes them with BART,
optionally explains in simple terms via OpenAI

## Run locally

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


export OPENAI_API_KEY=sk-...

uvicorn main:app --reload
```
