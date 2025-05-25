from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

class LLMRequest(BaseModel):
    context: list[str]  # list of document chunks as context
    question: str       # user query

class LLMResponse(BaseModel):
    generated_text: str

@app.post("/generate", response_model=LLMResponse)
async def generate_llm_response(req: LLMRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    # Compose messages for chat completion, including system prompt + user prompt + context
    system_message = {
        "role": "system",
        "content": "You are an AI assistant helping answer questions based on provided context."
    }

    # Combine context chunks as a single string
    context_text = "\n\n".join(req.context)

    user_message = {
        "role": "user",
        "content": f"Context:\n{context_text}\n\nQuestion: {req.question}"
    }

    payload = {
        "model": "gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo" depending on your access
        "messages": [system_message, user_message],
        "max_tokens": 500,
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OPENAI_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            return LLMResponse(generated_text=answer)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"OpenAI API request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"OpenAI API error: {e.response.text}")
