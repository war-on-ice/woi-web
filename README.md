# woi-web
WAR On Ice - Web

## Compile Instructions
1. Install vagrant and VirtualBox (or your favorite VM software)
2. Initialize a vagrant instance (I used "ubuntu/trusty64") - vagrant init ubuntu/trusty64
3. Open the Vagrantfile and forward the guest machine's port - config.vm.network "forwarded_port", guest: 5000, host: 5000
4. Start the vagrant box and ssh in
5. Create a virtual environment for the project
6. Install the requirements for this project - pip install -r requirements.txt
7. Run the flask file - python woi_frontend.py
8. Connect to localhost:5000 to see the site running!
