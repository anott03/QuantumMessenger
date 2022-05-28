# from python:3.11.0a4-alpine3.15 as base
# from qiskit/qiskit-runtime as base
from qiskit/qiskit-runtime

# from base as test
# workdir /test
# copy src/* .
# copy test/* .
# copy requirements_test .
# run --mount=type=cache,target=/test/.cache ["pip", "install", "pytest"]
# entrypoint ["pytest"]

# from base as run
copy requirements /app/requirements
copy ./src /app/src
# run --mount=type=cache,target=/app/.cache ["pip", "install", "-r", "requirements"]
run --mount=type=cache,target=/app/.cache ["pip", "install", "fastapi", "pydantic", "uvicorn"]

workdir /app/src/api
entrypoint ["uvicorn", "main:app"]
# entrypoint ["ls", "/app/src"]
