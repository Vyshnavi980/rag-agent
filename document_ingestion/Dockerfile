FROM python:3.9-slim
WORKDIR /app
COPY main.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt uvicorn[standard]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
