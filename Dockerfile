# Use a lightweight Python base image
FROM python:3.13-slim

# Prevent writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (Git, Pandoc, Make)
# We accept the default pandoc from Debian repositories for stability
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    pandoc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ruby gem dependencies
RUN gem install asciidoctor

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application logic into the container
COPY . .

# By default, provide a shell, but this can be overridden to run make
CMD ["/bin/bash"]