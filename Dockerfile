FROM python:3.9.12-slim-buster 

WORKDIR /app 

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    DJANGO_DEBUG=0 \
    PYPPETEER_HOME=/app

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev python3-dev curl tk
# for Chromium
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pyppeteer-install 

COPY . .

# add and run as non-root user
RUN useradd -u 8877 john
USER john

# shell form to get the port variable
CMD gunicorn -b 0.0.0.0:$PORT cardify.wsgi:application