# -------------------------------------------------------
# Base image
# -------------------------------------------------------
# We use the official slim Python 3.11 image.
# "slim" keeps the image small while still supporting compiled packages.
FROM python:3.11-slim


# -------------------------------------------------------
# Working directory inside the container
# -------------------------------------------------------
# All project files will live in /app
WORKDIR /app


# -------------------------------------------------------
# Python runtime behavior
# -------------------------------------------------------
# Prevents creation of .pyc files (saves disk, avoids stale bytecode bugs)
# Sends logs directly to Docker (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# -------------------------------------------------------
# System dependencies
# -------------------------------------------------------
# These are needed to build Python packages that include C extensions
# (e.g. pydantic, cryptography, numpy, etc)
# We remove apt cache afterward to keep the image small.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


# -------------------------------------------------------
# Copy project files into the container
# -------------------------------------------------------
# This must happen BEFORE pip install, because:
# - Your project is defined by pyproject.toml
# - The "app" package must exist for pip to install it
COPY . .


# -------------------------------------------------------
# Upgrade pip
# -------------------------------------------------------
# Old pip versions have bugs with pyproject.toml and wheels
RUN pip install --upgrade pip


# -------------------------------------------------------
# Install the application + test dependencies
# -------------------------------------------------------
# ".[test]" tells pip to install:
#   - Normal runtime dependencies from [project.dependencies]
#   - Test tools from [project.optional-dependencies.test]
#
# This is what makes pytest, pytest-cov, etc available inside Docker.
RUN pip install .[test]


# -------------------------------------------------------
# Security: run as a non-root user
# -------------------------------------------------------
# Running as root inside containers is a security risk.
# We create an unprivileged user and switch to it.
RUN adduser --disabled-password --gecos '' appuser
USER appuser


# -------------------------------------------------------
# Networking
# -------------------------------------------------------
# FastAPI will listen on port 8000
EXPOSE 8000


# -------------------------------------------------------
# Container startup command
# -------------------------------------------------------
# Uvicorn runs your FastAPI app
# "main:app" means: from main.py import app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
