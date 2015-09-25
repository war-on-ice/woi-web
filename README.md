# woi-web
WAR On Ice - Web

## Compile Instructions
1. Install vagrant and VirtualBox (or your favorite VM software)
2. Spin up vagrant instance from Vagrantfile `vagrant up`
4. SSH into vagrant box: `vagrant ssh`
5. Create a virtual environment for the project (optional)
6. Install the requirements for this project `pip install -r required.txt`
7. You will need to copy the config file and rename it to config.py. Update the username/password/server/db-name to your credentials.
7. Run the flask file - `python run.py`
8. Connect to localhost:5000 to see the site running!
