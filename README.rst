chem_lab_server
---------------
The REST API server for the Chem Lab Notebook project for CPTR 450. Built with Django 2, the Django REST Framework, and Python 3.7.

<<<<<<< HEAD
=======

>>>>>>> develop
Local Deployment
----------------
Use these steps to setup your local development environment.

MySQL
+++++
MySQL is automatically installed within Vagrant. You should clone the git repository between steps 2 and 3. You will also have to run step 4 every time you pull an update from git.

Vagrant (Linux lab computers)
.............................
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

  mysql> CREATE DATABASE chemlab CHARACTER SET utf8 COLLATE utf8_bin;
   
Docker (Personal computers)
...........................
1. Install MySQL server

::

  $ docker run -d \
    -p 8889:3306 \
    -e MYSQL_ROOT_PASSWORD=root \
    --name=mysql-cptr450 \
    mysql/mysql-server:5.7.22

2. Enter the MySQL command line, you may need to restart the container first

::

  $ docker exec -it mysql-server mysql -uroot -proot

3. Give the root user permission on localhost

::

  mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';

4. Create the Django table

::

  mysql> CREATE DATABASE chemlab CHARACTER SET utf8 COLLATE utf8_bin;


Local Django Setup
++++++++++++++++++
1. Install pipenv

::

  $ pip install pipenv

<<<<<<< HEAD
Django Setup
++++++++++++
1. Install dependencies
=======
2. Install dependencies
>>>>>>> develop

::

  $ pipenv install

Note: on MacOS the MySQL driver may need to be installed and can cause issues. Using brew to install MySQL will usually fix this.

3. Run migrations

::

  $ pipenv run python manage.py migrate

4. Run server

::

  $ pipenv run python manage.py runserver

