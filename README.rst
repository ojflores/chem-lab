django-server
-------------
The REST API server for the Chem Lab Notebook project for CPTR 450. Built with Django 2, the Django REST Framework, and Python 3.7.

Local Deployment
----------------
Use these steps to setup your local developemnt environment.

MySQL
+++++
MySQL can be installed with Docker. Use MySQL version 5.7.22.

Docker
......

1. Install MySQL server

::

  $ docker run -d \
    -p 8889:3306 \
    -e MYSQL_ROOT_PASSWORD=root \
    --name=mysql-server \
    mysql/mysql-server:5.7.22

2. Enter the MySQL command line, you may need to restart the container first

::

  $ docker exec -it mysql-server mysql -uroot -proot

3. Give the root user permission on localhost

::

  mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';

Database Setup
..............
1. Create the databases, use Docker step 2 to enter the MySQL command line if necessary

::

  mysql> CREATE DATABASE chemlab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



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

