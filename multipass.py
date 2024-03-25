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
    """
    Generate a random name for a new instance.

    Returns:
        str: A random name for a new instance.

    Example:
        >>> instance_name_gen()
        'xzv3a4'
    """
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))



def exec_command(name, command):
    """
    Execute a command on a specified instance.

    Args:
        name (str): The name of the instance on which to execute the command.
        command (str): The command to execute.

    Returns:
        bool: True if the command executed successfully, False otherwise.

    Example:
        >>> exec_command("instance_name", "ls")
        True
        >>> exec_command("instance_name", "ls /nonexistent")
        False
    """
    result = subprocess.run(["multipass", "exec", name, "--", command], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def run_shell(name):
    """
    Open a shell on a specified instance.

    Args:
        name (str): The name of the instance on which to open the shell.

    Example:
        >>> run_shell("instance_name")
    """
    subprocess.run(["multipass", "shell", name], check=True)



def launch_instance(name="default_name", image="22.04", cpus="1", memory="2G"):
    """
    Launch a new instance with the specified parameters.

    Args:
        name (str): The name of the instance to create.
        image (str): The image to use for the instance. Default is "22.04", <remote> can be used to fetch image from the internet.
        cpus (str): The number of CPUs to allocate to the instance.
        memory (str): The amount of memory to allocate to the instance.

    Returns:
        bool: True if the instance was created successfully, False otherwise.

    Example:
        >>> launch_instance("instance_name", "22.04", "1", "2G")
        True
    """
    result = subprocess.run(["multipass", "launch", "--name", name, "--cpus", cpus, "--memory", memory, image], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def stop_instance(name):
    """
    Stop a specified instance.

    Args:
        name (str): The name of the instance to stop.

    Returns:
        bool: True if the instance was stopped successfully, False otherwise.

    Example:
        >>> stop_instance("instance_name")
        True
    """
    result = subprocess.run(["multipass", "stop", name], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def start_instance(name):
    """
    Start a specified instance.

    Args:
        name (str): The name of the instance to start.

    Returns:
        bool: True if the instance was started successfully, False otherwise.

    Example:
        >>> start_instance("instance_name")
        True
    """
    result = subprocess.run(["multipass", "start", name], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def delete_instance(name):
    """
    Delete a specified instance.

    Args:
        name (str): The name of the instance to delete.

    Returns:
        bool: True if the instance was deleted successfully, False otherwise.

    Example:
        >>> delete_instance("instance_name")
        True
    """
    result = subprocess.run(["multipass", "delete", name, "--purge"], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def delete_all_instances():
    """
    Delete all instances.

    Returns:
        bool: True if all instances were deleted successfully, False otherwise.

    Example:
        >>> delete_all_instances()
        True
    """
    result = subprocess.run(["multipass", "delete", "--all", "--purge"], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance="Delete All Instances", error=result.stderr)
    return result.returncode == 0



def list_instances():
    """
    List all instances.

    Returns:
        list: A list of all instances.

    Example:
        >>> list_instances()
        ['instance1', 'instance2', 'instance3']
    """
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance="List Instances", error=result.stderr)
    return [line.split()[0] for line in result.stdout.split('\n')[2:] if line]



def get_ip(name):
    """
    Get the IP address of a specified instance.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The IP address of the instance.

    Example:
        >>> get_ip("instance_name")
        192.168.0.1
    """
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'IPv4' in line:
            return line.split()[1]
    return None



def get_state(name):
    """
    Get the state of a specified instance.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The state of the instance.

    Example:
        >>> get_state("instance_name")
        Running

        >>> get_state("stopped_instance")
        Stopped
    """
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'State' in line:
            return line.split()[1]
    return None



def put_file(name, source, destination):
    """
    Transfer a file to a specified instance.

    Args:
        name (str): The name of the instance.
        source (str): The path to the file to transfer.
        destination (str): The destination path on the instance.

    Returns:
        bool: True if the file was transferred successfully, False otherwise.

    Example:
        >>> put_file("instance_name", "file.txt", "/home/ubuntu/file.txt")
        True

        >>> put_file("instance_name", "nonexistent_file.txt", "/home/ubuntu/file.txt")
        False

        >>> put_file("instance_name", "file.txt", "/nonexistent/file.txt")
        False

        >>> put_file("nonexistent_instance", "file.txt", "/home/ubuntu/file.txt")
        False
    """
    result = subprocess.run(["multipass", "transfer", source, f"{name}:{destination}"], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def get_file(name, source, destination):
    """
    Transfer a file from a specified instance.

    Args:
        name (str): The name of the instance.
        source (str): The path to the file to transfer.
        destination (str): The destination path on the host.

    Returns:
        bool: True if the file was transferred successfully, False otherwise.

    Example:
        >>> get_file("instance_name", "/home/ubuntu/file.txt", "file.txt")
        True

        >>> get_file("instance_name", "/nonexistent/file.txt", "file.txt")
        False

        >>> get_file("nonexistent_instance", "/home/ubuntu/file.txt", "file.txt")
        False
    """
    result = subprocess.run(["multipass", "transfer", f"{name}:{source}", destination], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def mount(name, source, destination):
    """
    Mount a directory on the host to a specified instance.

    Args:
        name (str): The name of the instance.
        source (str): The path to the directory on the host.
        destination (str): The destination path on the instance.

    Returns:
        bool: True if the directory was mounted successfully, False otherwise.

    Example:
        >>> mount("instance_name", "/path/to/directory", "/mnt/directory")
        True

        >>> mount("instance_name", "/nonexistent/directory", "/mnt/directory")
        False
    """
    result = subprocess.run(["multipass", "mount", source, f"{name}:{destination}"], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def unmount(name):
    """
    Unmount a directory from a specified instance.

    Args:
        name (str): The name of the instance.

    Returns:
        bool: True if the directory was unmounted successfully, False otherwise.

    Example:
        >>> unmount("instance_name")
        True
    """
    result = subprocess.run(["multipass", "unmount", name], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.returncode == 0



def get_image(name):
    """
    Get the image of a specified instance.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The image of the instance.

    Example:
        >>> get_image("instance_name")
        22.04
    """
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'Image' in line:
            return line.split()[1]
    return None



def get_cpu_usage(name):
    """
    Get the CPU usage of a specified instance.
    Usage is calculated as the percentage of time the CPU is not idle.
    0.4 is equal to 40% CPU usage.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The CPU usage of the instance.

    Example:
        >>> get_cpu_usage("instance_name")
        0.0
    """
    result = subprocess.run(["multipass", "exec", name, "--", "mpstat", "1", "1"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'all' in line:
            return line.split()[2]
    return None



def get_memory_usage(name):
    """
    Get the memory usage of a specified instance.
    Usage is calculated in MB.
    10 is equal to 10MB memory usage.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The memory usage of the instance.

    Example:
        >>> get_memory_usage("instance_name")
        0
    """
    result = subprocess.run(["multipass", "exec", name, "--", "free", "-m"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'Mem' in line:
            return line.split()[2]
    return None



def get_disk_usage(name):
    """
    Get the disk usage of a specified instance.
    Usage is calculated in GB.
    0.8 is equal to 0.8GB disk usage.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The disk usage of the instance.

    Example:
        >>> get_disk_usage("instance_name")
        0.4
    """
    result = subprocess.run(["multipass", "exec", name, "--", "df", "-h"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if '/dev/root' in line:
            return line.split()[2]
    return None



def get_uptime(name):
    """
    Get the uptime of a specified instance.
    Uptime is formatted as days:hours:minutes.
    1:23:45 is equal to 1 day, 23 hours, and 45 minutes.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The uptime of the instance.

    Example:
        >>> get_uptime("instance_name")
        1:23:45
    """
    result = subprocess.run(["multipass", "exec", name, "--", "uptime"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.stdout.split(',')[0]



def get_processes(name):
    """
    Get the number of processes running on a specified instance.
    Number of processes is calculated as the number of lines in the output of the 'ps aux' command.

    Args:
        name (str): The name of the instance.

    Returns:
        int: The number of processes running on the instance.

    Example:
        >>> get_processes("instance_name")
        10
    """
    result = subprocess.run(["multipass", "exec", name, "--", "ps", "aux"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return len(result.stdout.split('\n')) - 1



def get_nb_users(name):
    """
    Get the number of users logged in to a specified instance.
    Number of users is calculated as the number of lines in the output of the 'who' command.

    Args:
        name (str): The name of the instance.

    Returns:
        int: The number of users logged in to the instance.

    Example:
        >>> get_nb_users("instance_name")
        1
    """
    result = subprocess.run(["multipass", "exec", name, "--", "who"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return len(result.stdout.split('\n')) - 1



def get_hostname(name):
    """
    Get the hostname of a specified instance.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The hostname of the instance.

    Example:
        >>> get_hostname("instance_name")
        "instance_hostname"
    """
    result = subprocess.run(["multipass", "exec", name, "--", "hostname"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.stdout.strip()



def get_running_instances():
    """
    Get the names of all running instances.

    Returns:
        list: A list of the names of all running instances.

    Example:
        >>> get_running_instances()
        ["instance1", "instance2"]
    """
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance="get_running_instances", error=result.stderr)
    return [line.split()[0] for line in result.stdout.split('\n') if "Running" in line]



def get_stopped_instances():
    """
    Get the names of all stopped instances.

    Returns:
        list: A list of the names of all stopped instances.

    Example:
        >>> get_stopped_instances()
        ["instance3", "instance4"]
    """
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance="get_running_instances", error=result.stderr)
    return [line.split()[0] for line in result.stdout.split('\n') if "Stopped" in line]



def get_all_instances():
    """
    Get the names of all instances, both running and stopped.

    Returns:
        list: A list of the names of all instances.

    Example:
        >>> get_all_instances()
        ["instance1", "instance2", "instance3", "instance4"]
    """
    running_instances = get_running_instances()
    stopped_instances = get_stopped_instances()
    return running_instances + stopped_instances



def get_instance_info(name):
    """
    Get information about a specified instance.

    Args:
        name (str): The name of the instance.

    Returns:
        str: Information about the instance.

    Example:
        >>> get_instance_info("instance_name")
        "Name:           instance_name
        State:          Running
        IPv4:           10.217.3.139
        Release:        Ubuntu 20.04.1 LTS
        Image hash:     26c2c19996c8 (Ubuntu 20.04 LTS)
        Load:           0.45 0.13 0.05
        Disk usage:     1.1G out of 4.7G
        Memory usage:   91.5M out of 985.4M"
    """
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    return result.stdout
