# Use official Python runtime as base image
FROM python:3.9-slim

# Accept API key as a build argument
ARG GEMINI_API_KEY
ARG NLTK_DOWNLOAD_DIR=/usr/local/share/nltk_data

# Set the environment variables
ENV GEMINI_API_KEY=$GEMINI_API_KEY
ENV NLTK_DATA=$NLTK_DOWNLOAD_DIR

# Create a non-root user
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create NLTK data directory and set permissions
RUN mkdir -p $NLTK_DOWNLOAD_DIR && \
    chown -R appuser:appuser $NLTK_DOWNLOAD_DIR

# Switch to non-root user for NLTK download
USER appuser

# Download NLTK data
RUN python -c "import nltk; \
    nltk.download('punkt', download_dir='$NLTK_DOWNLOAD_DIR'); \
    nltk.download('vader_lexicon', download_dir='$NLTK_DOWNLOAD_DIR'); \
    nltk.download('averaged_perceptron_tagger', download_dir='$NLTK_DOWNLOAD_DIR')"

# Download spacy english model
RUN python -m spacy download en_core_web_sm

# Switch back to root to copy project files
USER root

# Copy the entire project
COPY --chown=appuser:appuser . .

# Set permissions
RUN chmod +x start.sh && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 7860 8000

# Use the start script
CMD ["./start.sh"]