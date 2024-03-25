##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## taker instance library for taker instance information
## @julesreyn
##

from lib.taker_logger import logger
import subprocess


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