# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and ai-layer (since they are siblings and backend depends on ai-layer)
COPY backend /app/backend
COPY ai_layer /app/ai_layer

# Set PYTHONPATH to include the root so imports work
ENV PYTHONPATH=/app

WORKDIR /app/backend
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
