# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Environment variables
# PYTHONDONTWRITEBYTECODE → Prevents Python from writing .pyc files
# PYTHONUNBUFFERED → Forces stdout/stderr to be sent straight to the terminal (useful for logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required to build Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------
# Copy the full project into the container
# This MUST come before pip install because:
# your pyproject.toml defines a package that lives in "app/"
# pip cannot install it unless the source code exists.
# -------------------------------------------------------
COPY . .

# Upgrade pip to avoid old build bugs
RUN pip install --upgrade pip

# Install your project as a package (from pyproject.toml)
# This makes "app", "main", etc available in Python's site-packages
RUN pip install .

# -------------------------------------------------------
# Security: create a non-root user
# -------------------------------------------------------
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
