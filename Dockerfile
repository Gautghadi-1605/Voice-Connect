# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and source code
COPY requirements.txt .
COPY fastwapi.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Cloud Run port
ENV PORT 8080

# Expose port (optional for documentation)
EXPOSE 8080

# Run FastAPI with uvicorn, binding to the PORT environment variable
CMD ["sh", "-c", "uvicorn fastwapi:app --host 0.0.0.0 --port $PORT"]



