FROM python:3.12-slim

COPY . ./kv_api

WORKDIR /kv_api

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/kv_api

RUN pip install poetry && poetry config virtualenvs.create false && poetry lock --no-update && pip install --upgrade pip setuptools wheel && poetry install --no-dev

RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    cmake \
    git \
    build-essential \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN poetry add asynctnt

CMD ["poetry", "run", "python", "main.py"]

