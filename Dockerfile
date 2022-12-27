# syntax=docker/dockerfile:1
FROM python:3.7-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "detector.py"]
EXPOSE 5000
