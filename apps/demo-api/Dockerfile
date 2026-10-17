FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .


RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    rm -rf /usr/local/lib/python3.13/site-packages/pip \
           /usr/local/lib/python3.13/site-packages/pip-*.dist-info \
           /usr/local/bin/pip \
           /usr/local/bin/pip3 \
           /usr/local/bin/pip3.13


COPY app/ ./app/

RUN useradd --create-home --uid 10001 appuser && \
    chown -R appuser:appuser /app

USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
