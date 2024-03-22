##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## multipass library
## @julesreyn
##

from multipass import *
import secrets
import string

INSTANCE_IMAGE = "22.04"
INSTANCE_CPUS = "1"
INSTANCE_MEMORY = "2G"

def instance_name_gen():
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))

# def init_cloudflare_service():
    #TO-DO

# def update_motd(name):
    # TO-DO

# def install_prerequisites(name):
#     exec_command(name, "sudo apt update -y && sudo apt upgrade -y")

#     ## Install Python3, Python3-pip
#     exec_command(name, "sudo apt install  python3 python3-pip -y")

#     ## Install NodeJS, NVM
#     exec_command(name, "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash")
#     exec_command(name, "export NVM_DIR='$HOME/.nvm'; [ -s '$NVM_DIR/nvm.sh' ] && \. '$NVM_DIR/nvm.sh'; [ -s '$NVM_DIR/bash_completion' ] && \. '$NVM_DIR/bash_completion' ")
#     exec_command(name, "nvm install 20")

#     ## Install Docker and Docker Compose
#     exec_command(name, "sudo apt-get update; sudo apt-get install ca-certificates curl; sudo install -m 0755 -d /etc/apt/keyrings; sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc; sudo chmod a+r /etc/apt/keyrings/docker.asc; echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null; sudo apt-get update")
#     exec_command(name, "sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y; sudo curl -L 'https://github.com/docker/compose/releases/download/2.25.0/docker-compose-$(uname -s)-$(uname -m)' -o /usr/local/bin/docker-compose; sudo chattr +i /etc/hostname; sudo apt update -y && sudo apt upgrade -y")

#     ## Install Cloudflare service
#     exec_command(name, "sudo mkdir -p --mode=0755 /usr/share/keyrings; curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null; echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/cloudflared.list; sudo apt-get update -y && sudo apt-get install cloudflared -y")
#     put_file(name, "/home/jules/.cloudflared/cert.pem", "/home/ubuntu/.cloudflared/cert.pem")

def install_prerequisites(name):
    print("Putting files")
    put_file(name, "/home/dsi/mp/config_init.sh", "config_init.sh")
    print("Executing chmod")
    exec_command(name, "chmod +x /home/ubuntu/config.sh")
    print("Executing config.sh")
    exec_command(name, "./home/ubuntu/config.sh")
    print("Removing config.sh")
    exec_command(name, "rm /home/ubuntu/config.sh")
    print("Done")
    exec_command(name, "exit")

def init_instance(image=INSTANCE_IMAGE, cpu=INSTANCE_CPUS, memory=INSTANCE_MEMORY):
    name = instance_name_gen()
    launch_instance(name, image, cpu, memory)
    install_prerequisites(name)
    return name


if __name__ == "__main__":
    init_instance()