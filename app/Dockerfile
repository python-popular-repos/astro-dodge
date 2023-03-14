FROM python:3.11-buster AS builder
WORKDIR /app
COPY . /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
COPY requirements.txt /app
CMD ["python3", "app.py"]
