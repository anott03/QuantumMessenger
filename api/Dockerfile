from python:3.11.0a4-alpine3.15
workdir /app
copy . .
run ["pip", "install", "fastapi", "qiskit[visualization]"]
entrypoint ["python3", "main.py"]
