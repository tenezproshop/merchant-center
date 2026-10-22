FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-server.txt
COPY . .
CMD ["python", "server.py"]
