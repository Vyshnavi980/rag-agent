from fastapi import FastAPI, UploadFile, HTTPException
import aiofiles
import httpx

app = FastAPI()

EMBEDDING_SERVICE_URL = "http://embedding_indexing:8002/embed"  # Match your Docker service & port

@app.post("/upload")
async def upload(file: UploadFile):
    try:
        contents = await file.read()
        text = contents.decode("utf-8")

        # Split text into chunks (e.g., 1000 chars)
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

        async with httpx.AsyncClient() as client:
            resp = await client.post(EMBEDDING_SERVICE_URL, json={"chunks": chunks})
            resp.raise_for_status()
            embedding_response = resp.json()

        return {"chunks_sent": len(chunks), "embedding_response": embedding_response}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Embedding service error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
