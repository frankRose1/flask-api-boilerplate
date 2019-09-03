FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0:8000 --access-logfile - "app.app:create_app()"