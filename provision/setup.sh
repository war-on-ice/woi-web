#!/bin/bash

echo "Provisioning virtual machine..."

echo "Install PIP"
apt-get install python-pip python-dev build-essential -y
pip install --upgrade pip
pip install --upgrade virtualenv

echo "Install Security"
apt-get install libffi-dev libssl-dev -y
pip install pyopenssl ndg-httpsclient pyasn1

echo "Install MySQLdb"
#apt-get build-dep python-mysqldb -y
apt-get install libmysqlclient-dev -y
pip install MySQL-python

# echo "Preparing MySQL"
# apt-get install debconf-utils -y /dev/null

# debconf-set-selections <<< "mysql-server mysql-server/root_password password 1234"
# debconf-set-selections <<< "mysql-server mysql-server/root_password_again password 1234"

# echo "Install MySQL"
# apt-get install mysql-server -y > /dev/null