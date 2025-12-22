# docupath


# AUTOMATED PRODUCTION DEPLOYMENTS
# set server user name 
/DocuPath/infra/bootstrap.sh
/DocuPath/infra/deploy.sh
/DocuPath/infra/hooks.json
/DocuPath/infra/systemd/github-webhook.service

# Run it once:
sudo bash infra/bootstrap.sh

# Add exicutable permissions (This runs every time GitHub pushes to main.)
chmod +x infra/deploy.sh

# install systemd service (auto-start on boot)
sudo cp infra/systemd/github-webhook.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable github-webhook
sudo systemctl start github-webhook


# GitHub Webhook (ONE TIME)
# GitHub → Repo → Settings → Webhooks
Payload URL: http://SERVER_IP:9000/hooks/deploy
Content-Type: application/json
Event: push


# Validation Checklist
#After setup:
systemctl status github-webhook
docker compose ps

# Then push code:
git push origin main


# check webhook is installed
which webhook

# If which webhook returns NOTHING, install it.
sudo apt update
sudo apt install -y webhook

# Then re-check:
which webhook

# Reload systemd & restart
sudo systemctl daemon-reload
sudo systemctl restart github-webhook

# Check status:
systemctl status github-webhook

# You want to see:
Active: active (running)




# Make sure the latest code has been pushed to github
git add .
git commit -m "latest commit"
git push



# login
ssh root@170.64.213.243

# password
@DocuPath1A

# if issues connecting to server via SSH (This will remove the old key for that IP.)
ssh-keygen -R 170.64.213.243



# Create a new user (replace deploy with your username):
sudo adduser prod_user

# prod_user password
57OA^o7xbr9^

# Add the user to the sudo group (optional, for administrative tasks):
sudo usermod -aG sudo prod_user

# Switch to the new user
sudo su - prod_user



# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker-Compose
sudo apt install docker.io docker-compose -y

# Optional: enable Docker to run without sudo
sudo usermod -aG docker $USER
newgrp docker





# Create SSH keys for authentication
# Generate an SSH key on your server:
ssh-keygen -t ed25519 -C "daniel.mccarty2213@gmail.com"

# password
X7t4ie3bj!

# Copy public key & # Add it to GitHub → Settings → SSH and GPG keys → New SSH key
cat ~/.ssh/id_ed25519.pub

# After that, you can test the connection:
ssh -T git@github.com

# Are you sure you want to continue connecting (yes/no/[fingerprint])? 
yes




# Create project directories
mkdir -p ~/DocuPath
cd ~/DocuPath

# Then clone/pull using SSH: (No password is needed after this.)
git clone git@github.com:dan-mccarty/DocuPath.git


# Navigate to the project repo
cd ~/DocuPath/repo

# Create a .env file for environment variables
# Create a .env file to store secrets and configuration:
touch .env
nano .env

# add required values
DEBUG=False
...

# Navigate to the project base
cd ~/DocuPath

# rename file to prevent being run
mv ./docker-compose.override.yml ./OBS-docker-compose.override.yml




# Make sure Docker is installed and accessible
# Check if prod_user can run Docker:
docker --version
docker-compose version

# If permission denied, add the user to the Docker group:
sudo usermod -aG docker prod_user
newgrp docker



# check make is installed
make --version

# If not installed, but can be installed with:
sudo apt install make





# Build the Docker containers
docker-compose build

# Run migrations
docker-compose run --rm web python manage.py migrate

# Create a superuser
docker-compose run --rm web python manage.py createsuperuser

# Collect static files
docker compose run --rm web python manage.py collectstatic --noinput

# Start the containers ( same as "make up")
docker compose up -d

# Check the status
docker compose ps
docker compose logs -f




# Open a browser: ( http://<server_ip_or_domain>/admin )
http://170.64.213.243/admin






# login
ssh prod_user@170.64.213.243

# password
57OA^o7xbr9^









