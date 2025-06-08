FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements_lb.txt
CMD ["python", "load_balancer1.py"] 
