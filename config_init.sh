#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

sudo apt install  python3 python3-pip -y

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

export NVM_DIR='$HOME/.nvm'; [ -s '$NVM_DIR/nvm.sh' ] && \. '$NVM_DIR/nvm.sh'; [ -s '$NVM_DIR/bash_completion' ] && \. '$NVM_DIR/bash_completion'

nvm install 20

sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo mkdir -p --mode=0755 /usr/share/keyrings

curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/cloudflared.list

sudo apt-get update -y && sudo apt-get install cloudflared -y