# Dockerfile

# ---- Builder Stage ----
# Use a full Python image to build dependencies
FROM python:3.9 as builder

WORKDIR /usr/src/app

# Install build tools
RUN apt-get update && apt-get install -y gcc g++

# Install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# ---- Final Stage ----
# Use a slim image for the final application
FROM python:3.9-slim

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash dcfuser

# Copy installed packages from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels

# Copy application code
COPY . .

# Set ownership and switch user
RUN chown -R dcfuser:dcfuser /app
USER dcfuser

# Expose port and run application (as before)
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]