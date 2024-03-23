#!/bin/bash
#
# Conseil Junior Taker - 2024
# mp [Ubuntu::22.04]
# File description:
# Virtual machine configuration script
# @julesreyn
#


echo -e "\n\n[+] Initializing configuration of instance\n\n"

sudo apt update -y
sudo apt upgrade -y

echo -e "\n\n[+] Installing python3 and pip3\n\n"

sudo apt install  python3 python3-pip -y

echo -e "\n\n[+] Installing nvm & nodejs v20:lts\n\n"

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
sleep 5
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
source ~/.bashrc
nvm install 20
sudo apt-get update

echo -e "\n\n[+] Installing docker\n\n"

sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

echo -e "\n\n[+] Installing cloudflare service\n\n"

sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update -y && sudo apt-get install cloudflared -y
mkdir -p ~/.cloudflared

echo -e "\n\n[+] Finished configuration of instance\n\n"
