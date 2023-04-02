FROM python:3.11-slim-bullseye AS builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY app/requirements.txt .
RUN python -m pip install --no-cache-dir --disable-pip-version-check --requirement requirements.txt
WORKDIR /astro-dodge
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:create_app()"]
