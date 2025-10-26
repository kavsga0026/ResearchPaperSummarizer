# Research Paper Summarizer

> **An AI-powered web app that summarizes academic research papers and explains them in simple terms — like you’re 10 years old.**  
> Built with **FastAPI**, **React**, and **Transformer-based NLP models**, this project bridges research comprehension with artificial intelligence.

---


This project extracts text from uploaded **PDF research papers**, splits them into logical sections , generates **section-wise summaries**, and provides a simplified explanation of each section using **OpenAI GPT** or a **local transformer model**.

It’s a **full-stack AI application** demonstrating your skills in:
- Natural Language Processing (NLP)
- Backend API design (FastAPI)
- Frontend UI (React + TailwindCSS)
- Database management (SQLite + SQLAlchemy)
- Deployment (Render + Vercel)

---

## Tech Stack

| Layer | Technologies |
|-------|---------------|
| **Frontend** | React.js, Tailwind CSS, Framer Motion, Axios |
| **Backend** | FastAPI, Uvicorn, SQLAlchemy |
| **AI/NLP** | Hugging Face Transformers (T5/BART), OpenAI GPT API |
| **Database** | SQLite |
| **Deployment** | Render (Backend), Vercel (Frontend) |

---

## Project Structure

ResearchPaperSummarizer/
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── db.py # Database configuration
│ ├── models/
│ │ ├── summarizer.py # Summarization logic using Hugging Face
│ │ ├── text_extractor.py # Extracts text from PDF (PyMuPDF)
│ │ └── init.py
│ ├── utils/
│ │ └── section_splitter.py # Splits extracted text by sections
│ ├── requirements.txt # Backend dependencies
│ └── .env # OpenAI API key (not committed)
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx # Main application UI
│ │ ├── api.js # API integration using Axios
│ │ ├── components/ # UI components (Loader, Uploader, etc.)
│ ├── package.json
│ ├── tailwind.config.js
│ └── vite.config.js
│
└── README.md

