FROM python:3.10.12
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8090
CMD ["python", "./app/main.py", "--host", "0.0.0.0", "--port", "8080"]