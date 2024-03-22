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

def install_prerequisites(name):
    print("Putting files")
    put_file(name, "/home/dsi/mp/config.sh", "config.sh")
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