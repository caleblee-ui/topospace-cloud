
FROM python:3.12-slim
WORKDIR /app
COPY . /app
ENV PYTHONUNBUFFERED=1 PORT=8787
EXPOSE 8787
CMD ["python","api/server.py"]
