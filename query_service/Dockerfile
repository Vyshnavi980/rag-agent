FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache /tmp/*

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
