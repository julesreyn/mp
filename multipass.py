##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## multipass library
## @julesreyn
##

import os

def exec_command(name, command):
    os.system(f"multipass exec {name} -- {command}")

def launch_instance(name="default_name", image="22.04", cpus="1", memory="2G"):
    os.system(f"multipass launch --name {name} --cpus {cpus} --memory {memory} {image}")

def list_instances():
    os.system("multipass list")

def stop_instance(name):
    os.system("multipass stop " + name)

def start_instance(name):
    os.system("multipass start " + name)

def delete_instance(name):
    os.system(f"multipass delete " + name + " --purge")

def delete_all_instances():
    os.system("multipass delete --all --purge")

def get_ip(name):
    os.system("fmultipass info " + name + " | grep IPv4 | awk '{print $2}'")

def get_state(name):
    os.system("multipass info " + name + " | grep State | awk '{print $2}'")

def get_image(name):
    os.system("multipass info " + name + " | grep Image | awk '{print $2}'")

def put_file(name, source, destination):
    os.system(f"multipass transfer {source} {name}:{destination}")

def get_file(name, source, destination):
    os.system(f"multipass transfer {name}:{source} {destination}")

def mount(name, source, destination):
    os.system(f"multipass mount {source} {name}:{destination}")

def unmount(name):
    os.system(f"multipass unmount {name}")

def get_cpu_usage(name):
    os.system("multipass exec " + name + " -- mpstat 1 1 | grep all | awk '{print $3}'")

def get_memory_usage(name):
    os.system("multipass exec " + name + " -- free -m | grep Mem | awk '{print $3}'")

def get_disk_usage(name):
    os.system("multipass exec " + name + " -- df -h | grep /dev/root | awk '{print $3}'")

def get_uptime(name):
    os.system("multipass exec " + name + " -- uptime | awk '{print $3}'")

def get_processes(name):
    os.system("multipass exec " + name + " -- ps aux | wc -l")

def get_nb_users(name):
    os.system("multipass exec " + name + " -- who | wc -l")

def get_hostname(name):
    os.system("multipass exec " + name + " -- hostname")

