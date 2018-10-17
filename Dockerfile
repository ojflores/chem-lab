FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN pip install pip==18.0 && \ 
    pip install django && \
    pip install djangorestframework && \
    pip install PyMySQL && \
    set -e && \
    adduser --system django

WORKDIR /home/django

COPY ./ /home/django/chem_lab_server

WORKDIR /home/django/chem_lab_server

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8080


USER django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
