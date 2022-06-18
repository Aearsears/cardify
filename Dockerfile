FROM python:3.9.12-slim-buster 

WORKDIR /app 

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000 \
    WEB_CONCURRENCY=3

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev python3-dev
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "./cardify.wsgi" ]