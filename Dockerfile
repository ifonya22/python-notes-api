FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ADD pyproject.toml uv.lock /app/

RUN uv sync --locked

RUN mkdir app

RUN mkdir app/certs

RUN openssl genrsa -out /app/app/certs/jwt-private.pem

RUN openssl rsa -in /app/app/certs/jwt-private.pem -outform PEM -pubout -out /app/app/certs/jwt-public.pem 

ADD . /app/