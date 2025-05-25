FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt first for caching
COPY requirements.txt .

# Install CPU-only PyTorch and torchvision explicitly (CPU wheels)
RUN pip install --no-cache-dir torch==2.1.1+cpu torchvision==0.16.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt uvicorn[standard]

# Install the rest of your dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . /app

EXPOSE 8003

# Start the FastAPI app using uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
