##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## multipass library
## @julesreyn
##

from lib import *

INSTANCE_IMAGE = "22.04"
INSTANCE_CPUS = "1"
INSTANCE_MEMORY = "2G"

def upload_config(name):
    put_file(name, "./setup_tools/config.sh", "config.sh")
    put_file(name, "./setup_tools/update-motd.d/00-header", "00-header")
    put_file(name, "./setup_tools/update-motd.d/10-help-text", "10-help-text")

def install_prerequisites(name):
    upload_config(name)
    exec_command(name, "bash /home/ubuntu/config.sh")
    exec_command(name, "rm /home/ubuntu/config.sh")
    put_file(name, "~/.cloudflared/cert.pem", "~/.cloudflared/cert.pem")

def init_instance(image=INSTANCE_IMAGE, cpu=INSTANCE_CPUS, memory=INSTANCE_MEMORY):
    name = instance_name_gen()
    launch_instance(name, image, cpu, memory)
    install_prerequisites(name)
    return name

if __name__ == "__main__":
    init_instance()