##
## Multipass Library - 2024
## mp [Ubuntu:22.04]
## File description:
## multipass instance library for multipass instance operations
## @julesreyn
##

from mp.logger import logger
import subprocess
import secrets
import string
import logging

log = logging.getLogger(__name__)



def instance_name_gen():
    """
    Generate a random name for a new instance.

    Returns:
        str: A random name for a new instance.

    Example:
        >>> instance_name_gen()
        'xzvyan'
    """
    instances_name = ''.join(secrets.choice(string.ascii_lowercase) for _ in range(6))
    log.info(f'Generated instance name: {instances_name}')
    return instances_name



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
    log.info(f'Executing command on instance {name}: {command}')
    command_list = command.split()
    process = subprocess.run(["multipass", "exec", name, "--"] + command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        logger(instance=name, error=process.stderr)
    return process.returncode == 0



def run_shell(name):
    """
    Open a shell on a specified instance.

    Args:
        name (str): The name of the instance on which to open the shell.

    Example:
        >>> run_shell("instance_name")
    """
    log.info(f'Opening shell on instance {name}')
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
    log.info(f'Launching instance {name} with image {image}, {cpus} CPUs, and {memory} memory')
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
    log.info(f'Stopping instance {name}')
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
    log.info(f'Starting instance {name}')
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
    log.info(f'Deleting instance {name}')
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
    log.info('Deleting all instances')
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
    log.info('Listing all instances')
    result = subprocess.run(["multipass", "list"], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logger(instance="List Instances", error=result.stderr)
    return [line.split()[0] for line in result.stdout.split('\n')[2:] if line]



def stop_all_instances():
    """
    Stop all instances.

    Returns:
        bool: True if all instances were stopped successfully, False otherwise.

    Example:
        >>> stop_all_instances()
        True
    """
    log.info('Stopping all instances')
    instances = list_instances()
    for instance in instances:
        stop_instance(instance)
    return True



def start_all_instances():
    """
    Start all instances.

    Returns:
        bool: True if all instances were started successfully, False otherwise.

    Example:
        >>> start_all_instances()
        True
    """
    log.info('Starting all instances')
    instances = list_instances()
    for instance in instances:
        start_instance(instance)
    return True



def delete_stopped_instances():
    """
    Delete all stopped instances.

    Returns:
        bool: True if all stopped instances were deleted successfully, False otherwise.

    Example:
        >>> delete_stopped_instances()
        True
    """
    log.info('Deleting all stopped instances')
    instances = list_instances()
    for instance in instances:
        if "Stopped" in subprocess.run(["multipass", "info", instance], capture_output=True, text=True).stdout:
            delete_instance(instance)
    return True