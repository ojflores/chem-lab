chem_lab_server
---------------
The REST API server for the Chem Lab Notebook project for CPTR 450. Built with Django 2, the Django REST Framework, and Python 3.7.


Local Deployment
----------------
Use these steps to setup your local development environment.

MySQL
+++++
MySQL is the database server for our API. You will need to install it and there 
are few options for how.

Linux VM
........
1. Enter the MySQL server shell

::

  $ mysql -uroot -proot

2. Create the chemlab database

::

  mysql> CREATE DATABASE chemlab CHARACTER SET utf8 COLLATE utf8_bin;
  
3. Press ctrl+D to exit the mysql shell
   
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

Linux VM
........
1. Generate your SSH keys

::

  $ ssh-keygen

2. Print your public key and add it to GitLab

::

  cat ~/.ssh/id_rsa.pub

3. Clone the project

::

  git clone git@gitlab.cs.wallawalla.edu:ChemLab/chem-lab-server.git
  
4. Setup up the chamlab tables

::

  $ python manage.py migrate
  
5. Start the development server

::

  $ python manage.py runserver
  
6. Run the tests with

::

  $ python manage.py test

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
  
Updating the database
+++++++++++++++++++++
In the case that the database models ever change, the best way to reconfigure 
your databse will be to recreate it.

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

Production Deployment
---------------------
Deploying in production is different than the local development.

1. Create a .env file in the project root.

::

  DJANGO_TAG=VERSION
  DJANGO_ENV=prod
  DJANGO_PORT=8000
  DJANGO_SECRET_KEY=SECRET_KEY_GOES_HERE
  MYSQL_ROOT_PASSWORD=ANY_SECURE_PASSWORD
  MYSQL_USER=django
  MYSQL_PASSWORD=ANY_OTHER_SECURE_PASSWORD
  MYSQL_HOST=database
  MYSQL_PORT=3306
  MYSQL_DATABASE=chemlab
  MYSQL_DIR=DIRECTORY_FOR_MYSQL_DATABASE
  STATIC_DIR=DIRECTORY_FOR_STATIC_FILES

2. Create a directory at 'DIRECTORY_FOR_STATIC_FILES' and put the django static files generate by 'python manage.py collectstatic' there.

3. Run the compose script

::

  docker-compose up

4. Configure the reverse proxy to proxy to port 8000 where Django runs and also serve the static files previously setup.
