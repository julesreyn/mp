##
## Multipass Library - 2024
## mp [Ubuntu:22.04]
## File description:
## multipass instance library for multipass instance information
## @julesreyn
##

from mp.logger import logger
import subprocess
import logging

log = logging.getLogger(__name__)


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
    log.info(f'Getting IP address of instance {name}')
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)

    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'IPv4' in line:
            ipv4 = line.split()[1]
            log.info(f'Instance {name} has IP address {ipv4}')
            return ipv4
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
    log.info(f'Getting state of instance {name}')
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'State' in line:
            state = line.split()[1]
            log.info(f'Instance {name} is {state}')
            return state
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
    log.info(f'Getting image of instance {name}')
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'Image' in line:
            image = line.split()[1]
            log.info(f'Instance {name} is using image {image}')
            return image
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
    log.info(f'Getting CPU usage of instance {name}')
    result = subprocess.run(["multipass", "exec", name, "--", "mpstat", "1", "1"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'all' in line:
            cpu_usage = line.split()[-1]
            log.info(f'Instance {name} has CPU usage {cpu_usage}')
            return cpu_usage
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
    log.info(f'Getting memory usage of instance {name}')
    result = subprocess.run(["multipass", "exec", name, "--", "free", "-m"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if 'Mem' in line:
            mem = line.split()[2]
            log.info(f'Instance {name} has memory usage {mem}')
            return mem
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
    log.info(f'Getting disk usage of instance {name}')
    result = subprocess.run(["multipass", "exec", name, "--", "df", "-h"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    for line in result.stdout.split('\n'):
        if '/dev/root' in line:
            disk = line.split()[2]
            log.info(f'Instance {name} has disk usage {disk}')
            return disk
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
    log.info(f'Getting uptime of instance {name}')
    result = subprocess.run(["multipass", "exec", name, "--", "uptime"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'Instance {name} has uptime {result.stdout.split()[2]}')
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
    log.info(f'Getting number of processes on instance {name}')
    result = subprocess.run(["multipass", "exec", name, "--", "ps", "aux"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'Instance {name} has {len(result.stdout.split()) - 1} processes')
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
    log.info(f'Getting number of users on instance {name}')
    result = subprocess.run(["multipass", "exec", name, "--", "who"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'Instance {name} has {len(result.stdout.split()) - 1} users')
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
    log.info(f'Getting hostname of instance {name}')
    result = subprocess.run(["multipass", "exec", name, "--", "hostname"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'Instance {name} has hostname {result.stdout.strip()}')
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
    log.info('Getting running instances')
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance="get_running_instances", error=result.stderr)
    lines = result.stdout.split("\n")
    log.info(f'Running instances: [{", ".join([line.split()[0] for line in lines if "Running" in line])}]')
    return [line.split()[0] for line in lines if "Running" in line]



def get_stopped_instances():
    """
    Get the names of all stopped instances.

    Returns:
        list: A list of the names of all stopped instances.

    Example:
        >>> get_stopped_instances()
        ["instance3", "instance4"]
    """
    log.info('Getting stopped instances')
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance="get_running_instances", error=result.stderr)
    lines = result.stdout.split("\n")
    log.info(f'Stopped instances: [{", ".join([line.split()[0] for line in lines if "Stopped" in line])}]')
    return [line.split()[0] for line in lines if "Stopped" in line]



def get_all_instances():
    """
    Get the names of all instances, both running and stopped.

    Returns:
        list: A list of the names of all instances.

    Example:
        >>> get_all_instances()
        ["instance1", "instance2", "instance3", "instance4"]
    """
    log.info('Getting all instances')
    running_instances = get_running_instances()
    stopped_instances = get_stopped_instances()
    log.info(f'All instances: {running_instances + stopped_instances}')
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
    log.info(f'Getting information about instance {name}')
    result = subprocess.run(["multipass", "info", name], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'Information about instance {name}:\n{result.stdout}')
    return result.stdout
