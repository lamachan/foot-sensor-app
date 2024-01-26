FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y redis-server

COPY ./src /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080 6379

CMD ["bash", "-c", "redis-server & python app.py"]