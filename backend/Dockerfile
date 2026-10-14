FROM python:3.12-slim

WORKDIR /app

# Security: non-root user
RUN groupadd -r taskboard && useradd -r -g taskboard taskboard

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy alembic config
COPY alembic.ini .
COPY alembic/ alembic/

# Copy application
COPY app/ app/

# Change ownership
RUN chown -R taskboard:taskboard /app

USER taskboard

EXPOSE 8000

# Run migrations then start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
