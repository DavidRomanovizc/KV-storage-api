FROM python:3.12-slim

COPY . /auth

WORKDIR /auth

RUN pip install poetry && poetry config virtualenvs.create false && poetry lock --no-update && poetry install --no-dev

CMD ["poetry", "run", "python", "main.py"]
