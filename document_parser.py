import requests
import io
import fitz  # PyMuPDF
import docx
import email
from urllib.parse import urlparse

def download_file(url: str, timeout=30) -> bytes:
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content

def extract_text_from_pdf_bytes(bts: bytes) -> str:
    text = []
    with fitz.open(stream=bts, filetype="pdf") as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)

def extract_text_from_docx_bytes(bts: bytes) -> str:
    bio = io.BytesIO(bts)
    doc = docx.Document(bio)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)

def extract_text_from_eml_bytes(bts: bytes) -> str:
    msg = email.message_from_bytes(bts)
    parts = []
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            parts.append(part.get_payload(decode=True).decode(errors="ignore"))
        elif part.get_content_type() == "text/html":
            parts.append(part.get_payload(decode=True).decode(errors="ignore"))
    return "\n".join(parts)

def extract_text_from_url(url: str) -> str:
    content = download_file(url)
    path = urlparse(url).path.lower()
    if path.endswith(".pdf"):
        return extract_text_from_pdf_bytes(content)
    if path.endswith(".docx"):
        return extract_text_from_docx_bytes(content)
    if path.endswith(".eml"):
        return extract_text_from_eml_bytes(content)
    try:
        return extract_text_from_pdf_bytes(content)
    except Exception:
        try:
            return content.decode(errors="ignore")
        except:
            return ""

def clean_text(text: str) -> str:
    lines = text.split("\n")
    cleaned = [line.strip() for line in lines if line.strip()]
    return " ".join(cleaned)