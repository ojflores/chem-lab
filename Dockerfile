FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN pip install pip==18.0 && \ 
    #pip install pipenv==2018.7.1 && \
    #apk add mariadb-dev pcre pcre-dev && \
    #apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers libffi-dev && \
    #pip install uwsgi==2.0.17.1 && \
    pip install django && \
    pip install djangorestframework && \
    pip install PyMySQL && \
    set -e && \
    adduser --system django

WORKDIR /home/django

COPY ./ /home/django/chem_lab_server

WORKDIR /home/django/chem_lab_server

#RUN pipenv install --system --deploy --skip-lock --dev
#RUN pipenv install
#RUN pipenv run python -c "import django"

#ENV DJANGO_ENV=prod
ENV DJANGO_ENV=dev
ENV DOCKER_CONTAINER=1

EXPOSE 8080
EXPOSE 8889
EXPOSE 3306

#RUN apk del .build-deps

USER django
#CMD ["uwsgi", "--ini", "/home/django/chem_lab_server/uwsgi.ini"]
#CMD ["pipenv","run", "python", "manage.py", "runserver", "0.0.0.0:8080"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
