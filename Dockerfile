FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HTTP_HOST=0.0.0.0 \
    HTTP_PORT=8000

# Keep the dependency layer cached when only application code changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

CMD ["python", "-m", "backend.app"]
