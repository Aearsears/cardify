FROM python:3.9.12-slim-buster 

WORKDIR /app 

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    WEB_CONCURRENCY=3 \
    DJANGO_DEBUG=0

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev python3-dev curl tk
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# add and run as non-root user
RUN adduser -D myuser
USER myuser

CMD ["gunicorn"  , "-b", "0.0.0.0:$PORT", "cardify.wsgi:application"]