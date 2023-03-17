FROM python:3.11-slim-bullseye AS builder
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
COPY requirements.txt /app
CMD ["python3", "app.py"]
