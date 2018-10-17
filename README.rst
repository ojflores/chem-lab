django-server
-------------
The REST API server for the Chem Lab Notebook project for CPTR 450. Built with Django 2, the Django REST Framework, and Python 3.7.

Production Deployment
----------------
Use these steps to setups to activate the server on cptr450.cs.wallawalla.edu.

Django Setup
++++++++++++
1. Navigate to the correct directory

::

  $ cd home/chem-lab-server
  
2. Activate server

::

  $ pipenv run python manage.py runserver 0.0.0.0:8080

Local Deployment
----------------
Use these steps to setup your local developemnt environment.

MySQL
+++++
MySQL is automatically installed within Vagrant. You should clone the git repository between steps 2 and 3. You will also have to run step 4 every time you pull an update from git.

Vagrant (recommended)
.....................
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

Docker (alternative)
....................
1. Install MySQL server

::

  $ docker run -d \
    -p 8889:3306 \
    -e MYSQL_ROOT_PASSWORD=root \
    --name=mysql-server \
    mysql/mysql-server:5.7.22

2. Copy chemlab.sql to the container

::

  $ docker cp chemlab.sql mysql-server:/chemlab.sql

3. Enter the MySQL command line, you may need to restart the container first

::

  $ docker exec -it mysql-server mysql -uroot -proot

4. Give the root user permission on localhost

::

  mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';

5. Import chamlab.sql

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

