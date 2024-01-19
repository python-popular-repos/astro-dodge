FROM python:3.13.0a3-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY app/requirements.txt .
RUN python -m pip install --no-cache-dir --disable-pip-version-check --requirement requirements.txt
WORKDIR /astro-dodge
COPY . .
