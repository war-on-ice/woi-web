# woi-web
WAR On Ice - Web

## Compile Instructions
1. Install vagrant and VirtualBox (or your favorite VM software)
2. Spin up vagrant instance from Vagrantfile `vagrant up`
4. SSH into vagrant box: `vagrant ssh`
5. Create a virtual environment for the project (optional)
6. Install the requirements for this project `pip install -r required.txt`
7. You will need to create a file `cred.py` in the main directory. See below.
8. Run the flask file - `python run.py`
9. Connect to localhost:5000 to see the site running!

### Create cred.py
To the run application, you need to specify your database configuration. 
Create a file `cred.py` in the main application directory. This file should contain the following:

```
## MYSQL DB Credentials
mysql_username = "username"
mysql_password = "password"
mysql_server = "servername"
mysql_dbname = "dbname"
```