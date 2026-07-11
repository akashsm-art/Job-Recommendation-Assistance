FROM python:3.11-slim

# Install system dependencies needed for compiling psycopg2 and general operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend codebase
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000

# Run uvicorn app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
