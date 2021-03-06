Chem-lab Server
---------------
The REST API server for the Chem Lab Notebook project for CPTR 450. Built with Django 2, the Django REST Framework, and Python 3.7.

Refer to the wiki for implementation details.

Local Deployment
----------------
Use these steps to setup your local development environment.

MySQL
+++++
MySQL is the database server for our API. You will need to install it and there 
are few options for how.
   
Docker
......
1. Install Docker

Download your OS' Docker version here_ and install it. You will need to make an 
account. Linux users can probably install it with your respective package 
manager.

.. _here: https://store.docker.com/search?type=edition&offering=community

2. Install MySQL server

::

  $ docker run -d \
    -p 8889:3306 \
    -e MYSQL_ROOT_PASSWORD=root \
    --name=mysql-cptr450 \
    mysql/mysql-server:5.7.24

3. Enter the MySQL command line, you may need to restart the container first

::

  $ docker exec -it mysql-cptr450 mysql -uroot -proot

4. Give the root user permission on localhost

::

  mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';

5. Create the chemlab table

::

  mysql> CREATE DATABASE chemlab CHARACTER SET utf8 COLLATE utf8_bin;


Local Django Setup
++++++++++++++++++
Django is what runs our server.

MacOS and Linux
...............
1. Install pipenv (make sure you use python 3, not 2)

::

  $ pip install pipenv

2. Install dependencies

On MacOS, use brew_ to install mysql and set two environment variables so 
pipenv can find the OpenSSL libraries. For Linux, the default package managers 
may work but you can install and use linuxbrew_ as well.

Install brew using the command in one of the above links then run these three 
commands:

.. _brew: https://brew.sh/
.. _linuxbrew: http://linuxbrew.sh/

::

  $ brew install mysql
  $ export LDFLAGS="-L/usr/local/opt/openssl/lib"
  $ export CPPFLAGS="-I/usr/local/opt/openssl/include"
  
After that you should be able to install the dependencies with pipenv.

::

  $ pipenv install

3. Run migrations

::

  $ pipenv run python manage.py migrate

4. Run server

::

  $ pipenv run python manage.py runserver

Migrating the database
++++++++++++++++++++++
In the case that the database models are slightly modified, you can run the migrations on your local database.

::

  $ python manage.py migrate

Dropping the database
+++++++++++++++++++++
In the case that the database models are heavily modified or your database just needs to be reset, you can copletely
recreate the database.

1. Enter the mysql shell

::

  $ mysql -uroot -proot

2. Drop the database

::

  mysql> DROP DATABASE chemlab;

3. Now recreate the database

::

  mysql> CREATE DATABASE chemlab CHARACTER SET utf8 COLLATE utf8_bin;

4. Exit the mysql shell with ctrl+D

5. Run the migrations

::

  python manage.py migrate
