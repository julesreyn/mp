##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## multipass library
## @julesreyn
##

import subprocess
import secrets
import string

def instance_name_gen():
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))

def exec_command(name, command):
    subprocess.run(["multipass", "exec", name, "--", command], check=True)

def run_shell(name):
    subprocess.run(["multipass", "shell", name], check=True)

def launch_instance(name="default_name", image="22.04", cpus="1", memory="2G"):
    subprocess.run(["multipass", "launch", "--name", name, "--cpus", cpus, "--memory", memory, image], check=True)

def list_instances():
    subprocess.run(["multipass", "list"], check=True)

def stop_instance(name):
    subprocess.run(["multipass", "stop", name], check=True)

def start_instance(name):
    subprocess.run(["multipass", "start", name], check=True)

def delete_instance(name):
    subprocess.run(["multipass", "delete", name, "--purge"], check=True)

def delete_all_instances():
    subprocess.run(["multipass", "delete", "--all", "--purge"], check=True)

def get_ip(name):
    subprocess.run(["multipass", "info", name, "|", "grep", "IPv4", "|", "awk", "'{print $2}'"], check=True)

def get_state(name):
    subprocess.run(["multipass", "info", name, "|", "grep", "State", "|", "awk", "'{print $2}'"], check=True)

def get_image(name):
    subprocess.run(["multipass", "info", name, "|", "grep", "Image", "|", "awk", "'{print $2}'"], check=True)

def put_file(name, source, destination):
    subprocess.run(["multipass", "transfer", source, f"{name}:{destination}"], check=True)

def get_file(name, source, destination):
    subprocess.run(["multipass", "transfer", f"{name}:{source}", destination], check=True)

def mount(name, source, destination):
    subprocess.run(["multipass", "mount", source, f"{name}:{destination}"], check=True)

def unmount(name):
    subprocess.run(["multipass", "unmount", name], check=True)

def get_cpu_usage(name):
    subprocess.run(["multipass", "exec", name, "--", "mpstat", "1", "1", "|", "grep", "all", "|", "awk", "'{print $3}'"], check=True)

def get_memory_usage(name):
    subprocess.run(["multipass", "exec", name, "--", "free", "-m", "|", "grep", "Mem", "|", "awk", "'{print $3}'"], check=True)

def get_disk_usage(name):
    subprocess.run(["multipass", "exec", name, "--", "df", "-h", "|", "grep", "/dev/root", "|", "awk", "'{print $3}'"], check=True)

def get_uptime(name):
    subprocess.run(["multipass", "exec", name, "--", "uptime", "|", "awk", "'{print $3}'"], check=True)

def get_processes(name):
    subprocess.run(["multipass", "exec", name, "--", "ps", "aux", "|", "wc", "-l"], check=True)

def get_nb_users(name):
    subprocess.run(["multipass", "exec", name, "--", "who", "|", "wc", "-l"], check=True)

def get_hostname(name):
    subprocess.run(["multipass", "exec", name, "--", "hostname"], check=True)

def get_running_instances():
    result = subprocess.run("multipass list | grep Running | awk '{print $1}'", shell=True, capture_output=True, text=True)
    return result.stdout.split()

def get_stopped_instances():
    result = subprocess.run("multipass list | grep Stopped | awk '{print $1}'", shell=True, capture_output=True, text=True)
    return result.stdout.split()

def get_all_instances():
    running_instances = get_running_instances()
    stopped_instances = get_stopped_instances()
    return running_instances + stopped_instances

def get_instance_info(name):
    result = subprocess.run(f"multipass info {name}", shell=True, capture_output=True, text=True)
    return result.stdout