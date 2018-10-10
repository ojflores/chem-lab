django-server
-------------
The REST API server for the Chem Lab Notebook project for CPTR 450. Built with Django 2, the Django REST Framework, and Python 3.7.

Local Deployment
----------------
Use these steps to setup your local developemnt environment.

MySQL
+++++
MySQL is automatically installed within Vagrant. You will have to run step 4 every time you pull an update from git.

Database Setup
......

1. Start Vagrant

::

  $ vagrant up

2. Enter Vagrant

::

  $ vagrant ssh

3. Enter mysql command line.

::

  $ mysql -u root -ptest123

4. Import database from .sql file

::

  mysql> source chemlab.sql

 
Django Setup
++++++++++++
1. Install dependencies

::

  $ pipenv install

2. Run migrations

::

  $ pipenv run python manage.py migrate

3. Run server

::

  $ pipenv run python manage.py runserver

