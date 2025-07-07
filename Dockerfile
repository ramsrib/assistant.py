FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .env .

# Copy the application
COPY main.py .

# Run the script by default
CMD ["python3", "main.py"]
