from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size_words=250, overlap_words=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size_words]
        chunks.append(" ".join(chunk))
        i += chunk_size_words - overlap_words
    return [c for c in chunks if c.strip()]

def embed_texts(texts):
    return MODEL.encode(texts, convert_to_numpy=True, show_progress_bar=False)

class VectorStore:
    def __init__(self, chunks):
        self.chunks = chunks
        self.embeddings = embed_texts(chunks)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def top_k_chunks_for_query(self, query, k=5):
        q_emb = embed_texts([query])
        D, I = self.index.search(q_emb, k)
        return [self.chunks[i] for i in I[0]], [float(D[0][j]) for j in range(k)]