FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Install python-telegram-bot directly (no requirements.txt needed)
RUN pip install --no-cache-dir python-telegram-bot

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app/bot
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8443

# Run the bot
CMD ["python", "bot/main.py"]