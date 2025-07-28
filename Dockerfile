# Use an official Python base image
FROM python:3.11-slim

# Install system dependencies for Tesseract OCR and PDF/image processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        poppler-utils \
        libgl1 \
        gcc \
        libsm6 \
        libxext6 \
        libxrender-dev \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY src/ src/
COPY input/ input/

# Create output directory (if not mounting)
RUN mkdir -p output

# Set environment variables (optional, for UTF-8 support)
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

# Set the entrypoint to run your main script
ENTRYPOINT ["python", "src/main.py"]
#hi