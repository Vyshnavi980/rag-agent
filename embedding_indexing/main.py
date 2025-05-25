import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import faiss
import asyncio

app = FastAPI()

# Dummy embedding function - replace with your real embedding model call
def get_embedding(text: str) -> np.ndarray:
    # For demo: convert text chars to float vector, pad/truncate to 128 dims
    vec = np.array([float(ord(c)) for c in text[:128]])
    if vec.size < 128:
        vec = np.pad(vec, (0, 128 - vec.size))
    return vec / np.linalg.norm(vec)

# Data structures to hold indexed data
embedding_dim = 128
index = faiss.IndexFlatIP(embedding_dim)  # Inner product (cosine similarity if normalized)
metadata = []  # list of dicts holding chunks & other info

class EmbedRequest(BaseModel):
    chunks: List[str]

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class SearchResult(BaseModel):
    chunk: str
    score: float

@app.post("/embed")
async def embed_chunks(req: EmbedRequest):
    embeddings = []
    for chunk in req.chunks:
        emb = get_embedding(chunk)
        embeddings.append(emb)
        metadata.append({"chunk": chunk})
    embeddings_np = np.vstack(embeddings).astype('float32')
    index.add(embeddings_np)
    return {"message": "Chunks embedded and indexed successfully", "indexed_count": len(req.chunks)}

@app.post("/search")
async def search(req: SearchRequest):
    if index.ntotal == 0:
        raise HTTPException(status_code=404, detail="No data indexed yet")

    query_emb = get_embedding(req.query).astype('float32').reshape(1, -1)
    D, I = index.search(query_emb, req.top_k)
    
    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        chunk_info = metadata[idx]
        results.append({"chunk": chunk_info["chunk"], "score": float(dist)})
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
