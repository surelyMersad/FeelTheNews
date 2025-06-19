# Use official Python slim image as base
FROM python:3.10-slim

# Install only essential system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        gcc \
        libssl-dev \
        pkg-config \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Use smaller Rust install directory and avoid modifying root home
ENV CARGO_HOME=/tmp/cargo
ENV RUSTUP_HOME=/tmp/rustup
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy only requirements first for better layer caching
COPY backend/requirements.txt .

# Install Python dependencies early
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY backend/ /app/

# Expose expected port
EXPOSE 10000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
