FROM python:3.11-slim

WORKDIR /app

# Install build deps if needed
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application
COPY . /app

# Expose port
EXPOSE 8000

# Default DB_PATH points to persistent mounted volume
ENV DB_PATH=/data/internship_app.db
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
