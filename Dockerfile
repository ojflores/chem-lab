FROM python:3.7-alpine3.8

MAINTAINER sheldon.woodward@wallawalla.edu 

RUN apk add mariadb-dev pcre pcre-dev && \
    apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers libffi-dev && \
    pip install pipenv==2018.10.13 && \
    pip install uwsgi==2.0.17.1 && \
    set -e && \
    adduser -S django

WORKDIR /home/django

COPY . chem_lab_server

WORKDIR /home/django/chem_lab_server
RUN pipenv install --system --deploy

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8000

RUN apk del .build-deps

USER django
CMD ["uwsgi", "--ini", "/home/django/chem_lab_server/uwsgi.ini"]

