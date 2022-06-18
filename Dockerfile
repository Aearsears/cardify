FROM python:3.9.12-slim-buster 

WORKDIR /app 

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=django_heroku.settings \
    PORT=8000 \
    WEB_CONCURRENCY=3

RUN sudo apt install libpq-dev python3-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "./cardify.wsgi" ]