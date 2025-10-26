from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.text_extractor import extract_text_from_pdf
from utils.section_splitter import extract_sections
from models.summarizer import summarize_text
from openai import OpenAI
from dotenv import load_dotenv
import os
import traceback
from transformers import pipeline
from db import Summary, Base, SessionLocal, engine
from typing import List

# Create DB tables if not present
Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Research Paper Summarizer API", version="2.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Research Paper Summarizer API is running"}


@app.post("/summarize")
async def summarize(pdf: UploadFile = File(...)):
    """Extract text from PDF and generate section summaries"""
    if not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a valid PDF file")

    text = extract_text_from_pdf(pdf)
    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Not enough text to summarize")

    sections = extract_sections(text)
    if not sections:
        sections = {"full_paper": text[:8000]}

    summaries = {}
    for section, content in sections.items():
        if len(content.split()) > 40:
            summaries[section] = summarize_text(content)

    # 🧩 Combine summaries to store in DB
    combined_summary = "\n\n".join(
        f"{k.upper()}:\n{v}" for k, v in summaries.items()
    )

    # 🧩 Save to SQLite database
    try:
        db = SessionLocal()
        entry = Summary(
            filename=pdf.filename,
            summary=combined_summary,
            mode="Normal"
        )
        db.add(entry)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        db.close()

    return {"summaries": summaries, "message": "Summary generated and saved successfully."}




@app.post("/explain")
async def explain_text(data: dict):
    """Simplify a summary using ChatGPT (Explain Like I’m 10)"""
    summary_text = data.get("summary", "")
    if not summary_text:
        raise HTTPException(status_code=400, detail="No summary text provided")

    print("\n[INFO] Received text for explanation:")
    print(summary_text[:200], "...\n")

    try:
        # Try OpenAI first
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly AI that explains research papers simply to a 10-year-old.",
                },
                {
                    "role": "user",
                    "content": f"Explain this in simple and detailed terms:\n{summary_text}",
                },
            ],
            max_tokens=250,
            temperature=0.7,
        )
        explanation = response.choices[0].message.content.strip()
        print("[INFO] Explanation generated successfully ✅")
        return {"explanation": explanation}

    except Exception as e:
        error_msg = str(e)
        print("\n[ERROR] Explain API failed:", error_msg)

        # If OpenAI quota exceeded, use a local fallback model
        if "insufficient_quota" in error_msg or "429" in error_msg:
            print("[WARN] OpenAI quota exceeded — using local fallback summarizer 🧠")
            try:
                local_model = pipeline("summarization", model="facebook/bart-large-cnn")
                simplified = local_model(
                    f"Simplify this text for a 10-year-old:\n{summary_text}",
                    max_length=100,
                    min_length=30,
                    do_sample=False
                )[0]["summary_text"]

                return {"explanation": simplified + " (local model)"}

            except Exception as local_err:
                print("[FATAL] Local fallback failed:", str(local_err))
                return {"explanation": "⚠️ Explanation unavailable right now (both models failed)."}

        # For other OpenAI errors (auth, invalid model, etc.)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {error_msg}")


@app.get("/history")
def history(limit: int = 10):
    """Fetch recent summaries"""
    db = SessionLocal()
    try:
        rows: List[Summary] = (
            db.query(Summary)
            .order_by(Summary.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "filename": r.filename,
                "mode": r.mode,
                "created_at": r.created_at.isoformat(),
                "summary": (r.summary[:500] + "...") if len(r.summary) > 500 else r.summary,
            }
            for r in rows
        ]
    finally:
        db.close()
