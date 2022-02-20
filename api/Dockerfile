from python:3.11.0a4-alpine3.15 as base

from base as test
workdir /test
copy src/* .
copy test/* .
copy requirements_test .
run --mount=type=cache,target=/test/.cache ["pip", "install", "-r", "requirements_test"]
entrypoint ["pytest"]

from base as run
workdir /app
copy . .
copy requirements .
run --mount=type=cache,target=/app/.cache ["pip", "install", "-r", "requirements"]
entrypoint ["python3", "src/main.py"]
