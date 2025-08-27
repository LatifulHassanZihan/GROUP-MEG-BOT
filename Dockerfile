FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    sqlite3 \
    pkg-config \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Copy requirements file
COPY requirements.txt .

# Debug: Show what's in requirements.txt
RUN echo "Contents of requirements.txt:" && cat requirements.txt

# Filter out problematic packages and install dependencies
RUN grep -v "^sqlite3" requirements.txt > requirements_filtered.txt || cp requirements.txt requirements_filtered.txt
RUN echo "Filtered requirements:" && cat requirements_filtered.txt
RUN pip install --no-cache-dir -r requirements_filtered.txt --verbose

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8443

# Run the bot
CMD ["python", "bot/main.py"]