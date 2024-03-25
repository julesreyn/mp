##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## multipass library
## @julesreyn
##

import subprocess
from taker_logger import logger
import secrets
import string

def instance_name_gen():
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))

def exec_command(name, command):
    result = subprocess.run(["multipass", "exec", name, "--", command], capture_output=True, text=True)
    return result.returncode == 0

def run_shell(name):
    subprocess.run(["multipass", "shell", name], check=True)


def launch_instance(name="default_name", image="22.04", cpus="1", memory="2G"):
    result = subprocess.run(["multipass", "launch", "--name", name, "--cpus", cpus, "--memory", memory, image], capture_output=True, text=True)
    return result.returncode == 0

def stop_instance(name):
    result = subprocess.run(["multipass", "stop", name], capture_output=True, text=True)
    return result.returncode == 0

def start_instance(name):
    result = subprocess.run(["multipass", "start", name], capture_output=True, text=True)
    return result.returncode == 0

def delete_instance(name):
    result = subprocess.run(["multipass", "delete", name, "--purge"], capture_output=True, text=True)
    return result.returncode == 0

def delete_all_instances():
    result = subprocess.run(["multipass", "delete", "--all", "--purge"], capture_output=True, text=True)
    return result.returncode == 0

def list_instances():
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    return [line.split()[0] for line in result.stdout.split('\n')[2:] if line]

def get_ip(name):
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    for line in result.stdout.split('\n'):
        if 'IPv4' in line:
            return line.split()[1]
    return None

def get_state(name):
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    for line in result.stdout.split('\n'):
        if 'State' in line:
            return line.split()[1]
    return None

def put_file(name, source, destination):
    result = subprocess.run(["multipass", "transfer", source, f"{name}:{destination}"], capture_output=True, text=True)
    return result.returncode == 0

def get_file(name, source, destination):
    result = subprocess.run(["multipass", "transfer", f"{name}:{source}", destination], capture_output=True, text=True)
    return result.returncode == 0

def mount(name, source, destination):
    result = subprocess.run(["multipass", "mount", source, f"{name}:{destination}"], capture_output=True, text=True)
    return result.returncode == 0

def unmount(name):
    result = subprocess.run(["multipass", "unmount", name], capture_output=True, text=True)
    return result.returncode == 0

def get_image(name):
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    for line in result.stdout.split('\n'):
        if 'Image' in line:
            return line.split()[1]
    return None

def get_cpu_usage(name):
    result = subprocess.run(["multipass", "exec", name, "--", "mpstat", "1", "1"], capture_output=True, text=True, check=True)
    for line in result.stdout.split('\n'):
        if 'all' in line:
            return line.split()[2]
    return None

def get_memory_usage(name):
    result = subprocess.run(["multipass", "exec", name, "--", "free", "-m"], capture_output=True, text=True, check=True)
    for line in result.stdout.split('\n'):
        if 'Mem' in line:
            return line.split()[2]
    return None
def get_disk_usage(name):
    result = subprocess.run(["multipass", "exec", name, "--", "df", "-h"], capture_output=True, text=True, check=True)
    for line in result.stdout.split('\n'):
        if '/dev/root' in line:
            return line.split()[2]
    return None

def get_uptime(name):
    result = subprocess.run(["multipass", "exec", name, "--", "uptime"], capture_output=True, text=True, check=True)
    return result.stdout.split(',')[0]

def get_processes(name):
    result = subprocess.run(["multipass", "exec", name, "--", "ps", "aux"], capture_output=True, text=True, check=True)
    return len(result.stdout.split('\n')) - 1

def get_nb_users(name):
    result = subprocess.run(["multipass", "exec", name, "--", "who"], capture_output=True, text=True, check=True)
    return len(result.stdout.split('\n')) - 1

def get_hostname(name):
    result = subprocess.run(["multipass", "exec", name, "--", "hostname"], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_running_instances():
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    return [line.split()[0] for line in result.stdout.split('\n') if "Running" in line]

def get_stopped_instances():
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    return [line.split()[0] for line in result.stdout.split('\n') if "Stopped" in line]

def get_all_instances():
    running_instances = get_running_instances()
    stopped_instances = get_stopped_instances()
    return running_instances + stopped_instances

def get_instance_info(name):
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    return result.stdout

def get_hostname(name):
    result = subprocess.run(["multipass", "exec", name, "--", "hostname"], capture_output=True, text=True, check=True)
    return result.stdout.strip()

print(get_ip(get_running_instances()[0]))