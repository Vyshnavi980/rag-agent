import os, logging, httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
logging.basicConfig(level=logging.INFO)

EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://embedding_indexing:8002")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://llm_service:8000")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest) -> QueryResponse:
    logging.info(f"Query received: {req.query}")
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(f"{EMBEDDING_SERVICE_URL}/search", json={"query": req.query, "top_k": 3}, timeout=10)
            r.raise_for_status()
            chunks = [item.get("chunk", "") for item in r.json().get("results", [])]
            if not chunks:
                logging.info("No chunks found")
                return QueryResponse(answer="No relevant documents found.")

            r = await client.post(f"{LLM_SERVICE_URL}/generate", json={"context": chunks, "question": req.query}, timeout=20)
            r.raise_for_status()
            answer = r.json().get("generated_text", "")
            if not answer:
                logging.warning("Empty LLM response")
                return QueryResponse(answer="LLM did not generate a response.")

            logging.info("Answer generated")
            return QueryResponse(answer=answer)

        except httpx.RequestError as e:
            logging.error(f"Request error: {e}")
            raise HTTPException(503, detail=f"Service unavailable: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error: {e.response.text}")
            raise HTTPException(e.response.status_code, detail=f"Error response: {e.response.text}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise HTTPException(500, detail=f"Internal error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
