from python:3.11.0a4-alpine3.15
workdir /app
copy . .
run ["pip", "install", "fastapi", "qiskit[visualization]", "pydantic"]
entrypoint ["python3", "src/main.py"]
