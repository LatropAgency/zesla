# pull official base image
FROM python:3.8.2-alpine3.11
# set environment varibles
ENV PYTHONUNBUFFERED=1
# set work directory
WORKDIR /app

# install psycopg2
RUN apk update \
    && apk add gcc musl-dev python3-dev libffi-dev libressl-dev openssl-dev py3-lxml\
    && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev libressl-dev openssl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps \
    && apk add xvfb \
    && apk add wkhtmltopdf

# copy requirements.txt
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# copy project
COPY . /app/
# run entrypoint.sh
CMD ./entrypoint.sh