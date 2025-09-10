FROM python:3.11-slim
RUN pip install --no-cache-dir psycopg[binary]==3.1.19
WORKDIR /app
COPY main.py /app/
CMD ["python", "main.py"]