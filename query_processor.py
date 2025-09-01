import os
import google.generativeai as genai

# Set your Gemini API key in the environment variable GEMINI_API_KEY
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Set your GEMINI_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_answer(question: str, context_chunks: list):
    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""
You are an assistant that MUST answer only using the provided context.
If the answer is not present in the context, respond exactly: "Information not available in provided document".
Provide a concise answer (1-3 sentences) and then a short "Rationale:" line referencing the clause/sentence you used from context.
Do NOT hallucinate.
Return a JSON:
{{
  "decision": "...",
  "amount": "...",
  "justification": "...",
  "source_clauses": ["..."]
}}

Context:
---
{context}
---
Question: {question}
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()