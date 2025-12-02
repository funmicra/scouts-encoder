# ----------------------------------------
# Build stage
# ----------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build essentials only for compiling dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source code (needed for wheels, etc.)
COPY . .

# ----------------------------------------
# Production stage
# ----------------------------------------
FROM python:3.12-slim

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only application files (exclude tests/docs if needed)
COPY --from=builder /app /app

# Optimize environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose application port
EXPOSE 5000

# Gunicorn entrypoint
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--threads", "2", "app:app"]
