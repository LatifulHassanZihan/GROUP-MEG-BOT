FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8443

# Run the bot (will fail if missing dependencies, but Docker will build)
CMD ["python", "bot/main.py"]