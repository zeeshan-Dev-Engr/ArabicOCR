# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Qari-OCR from GitHub
RUN pip install --no-cache-dir git+https://github.com/mush42/qari-ocr.git

# Copy project
COPY . .

# Create temp directory for file uploads
RUN mkdir -p ./temp && chmod 777 ./temp

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "app.main"]