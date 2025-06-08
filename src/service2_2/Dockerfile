FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    curl \
    git \
    build-essential

RUN pip install --upgrade pip

COPY requirements_service.txt .
RUN pip install --no-cache-dir -r requirements_service.txt

COPY . .

CMD ["python", "app.py"]