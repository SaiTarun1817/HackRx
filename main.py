from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from document_parser import extract_text_from_url, clean_text
from vector_store import chunk_text, VectorStore
from query_processor import generate_answer
from document_parser import extract_text_from_url, extract_text_from_pdf_bytes, clean_text
import os
import json

TEAM_TOKEN = "31fc25012e9fc7527b7477d46c55f9fddbf1fe223cc61365879f50f1bb1dd574"

app = FastAPI(title="HackRx Retrieval API")

class RunRequest(BaseModel):
    documents: list  # List of URLs or file paths
    questions: list

@app.post("/hackrx/run")
async def run_job(payload: RunRequest, authorization: str = Header(None)):
    # 1) Auth
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization")
    token = authorization.split(" ", 1)[1].strip()
    if token != TEAM_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    # 2) Extract and combine all docs
    all_text = ""
    for doc_path in payload.documents:
        if doc_path.lower().startswith("http"):
            text = extract_text_from_url(doc_path)
        else:
            with open(doc_path, "rb") as f:
                content = f.read()
            text = extract_text_from_pdf_bytes(content)
        all_text += "\n" + clean_text(text)

    if not all_text.strip():
        return {"answers": ["No text extracted from document(s)."]}

    # 3) Chunk & embed
    chunks = chunk_text(all_text, chunk_size_words=250, overlap_words=50)
    vs = VectorStore(chunks)

    answers = []
    for q in payload.questions:
        top_chunks, _ = vs.top_k_chunks_for_query(q, k=3)
        ans_text = generate_answer(q, top_chunks)
    # Extract only the main answer string if ans_text is JSON
        try:
            ans_clean = ans_text.strip()
            if ans_clean.startswith("```json"):
                ans_clean = ans_clean[7:]
            if ans_clean.endswith("```"):
                ans_clean = ans_clean[:-3]
            ans_json = json.loads(ans_clean)
            # Use the "decision" or main answer field
            answers.append(ans_json.get("decision", ans_clean))
        except Exception:
            answers.append(ans_text)
    return {"answers": answers}