FROM python:3.14.2-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY /app/requirements.txt /app/

RUN pip install -r /app/requirements.txt --no-cache-dir

WORKDIR /app