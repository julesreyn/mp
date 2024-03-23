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
import subprocess

# def exec_command(name, command):
#     result = os.system(f"multipass exec {name} -- {command}")
#     lines = result
#     for line in lines[:10]:
#         print(f"> {line}")

def install_prerequisites(name):
    print("[INFO] Uploading config.sh to instance.")
    put_file(name, "./config.sh", "config.sh")
    exec_command(name, "chmod +x /home/ubuntu/config.sh")
    print("[INFO] Starting configuration.")
    exec_command(name, "bash /home/ubuntu/config.sh")
    print("[INFO] Installation complete, removing config file")
    exec_command(name, "rm /home/ubuntu/config.sh")
    put_file(name, "~/.cloudflared/cert.pem", "~/.cloudflared/cert.pem")
    print("Done")

def init_instance(image=INSTANCE_IMAGE, cpu=INSTANCE_CPUS, memory=INSTANCE_MEMORY):
    name = instance_name_gen()
    launch_instance(name, image, cpu, memory)
    install_prerequisites(name)
    return name

if __name__ == "__main__":
    init_instance()