#!/usr/bin/env bash
set -e

PROJECT_NAME=DJANGO_STARTER
APP_USER=prod_user
APP_DIR=/home/$APP_USER/$PROJECT_NAME
DEPLOY_DIR=/home/$APP_USER/deploy

echo "🔧 Bootstrapping server..."

# ---- Create user (if missing)
if ! id "$APP_USER" &>/dev/null; then
  adduser --disabled-password --gecos "" $APP_USER
  usermod -aG sudo,docker $APP_USER
fi

# ---- Install dependencies
apt update
apt install -y docker.io docker-compose webhook ufw git

# ---- Firewall
ufw allow OpenSSH
ufw allow 80
ufw allow 443
ufw allow 9000
ufw --force enable

# ---- Directories
mkdir -p $DEPLOY_DIR
chown -R $APP_USER:$APP_USER /home/$APP_USER

echo "✅ Bootstrap complete. Log out & back in."
