# ----------------------------------------
# Production-ready Flask container
# ----------------------------------------
FROM python:3.12-slim

# Optimize environment for predictable behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build essentials only if needed (kept small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip to avoid dependency lookup issues
RUN python -m pip install --upgrade pip

# Install dependencies, including Gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 5000

# Gunicorn entrypoint
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--threads", "2", "app:app"]
