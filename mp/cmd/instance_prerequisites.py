##
## Multipass Library - 2024
## mp [Ubuntu:22.04]
## File description:
## multipass instance library for multipass instance initialization
## @julesreyn
##

from mp.cmd.instance_operations import instance_name_gen, exec_command
from mp.cmd.instance_operations import launch_instance
from mp.cmd.file_operations import put_file
import subprocess
import socket
import logging

log = logging.getLogger(__name__)

DEFAULT_INSTANCE_IMAGE = "22.04" # available options: 20.04, 22.04, 23.10, daily:24.04, docker, jellyfin, core, core18, core20, core22  -> search new image with "multipass find"
DEFAULT_INSTANCE_VCPUS = "1" # available options: 1, 2, 4, 6, more..
DEFAULT_INSTANCE_MEMORY = "2G" # available options: 512M, 1G, 2G, 4G, 8G, more..

def upload_config(name):
    """
    Uploads the configuration files to the instance

    Args:
        name (str): The name of the instance

    Returns:
        None

    Example:
        >>> upload_config("instance_name")
    """
    log.info(f'Uploading configuration files to instance {name}')
    log.info(f'Uploading config.sh to instance {name}')
    put_file(name, "./setup_tools/config.sh", "config.sh")
    log.info(f'Uploading update-motd.d/00-header to instance {name}')
    put_file(name, "./setup_tools/update-motd.d/00-header", "00-header")
    log.info(f'Uploading update-motd.d/10-help-text to instance {name}')
    put_file(name, "./setup_tools/update-motd.d/10-help-text", "10-help-text")


def install_prerequisites(name):
    """
    Installs the prerequisites on the instance

    Args:
        name (str): The name of the instance

    Returns:
        None

    Example:
        >>> install_prerequisites("instance_name")
    """
    log.info(f'Installing prerequisites on instance {name}')
    upload_config(name)
    log.info(f'Adding execution permissions to config.sh on instance {name}')
    exec_command(name, "chmod +x /home/ubuntu/config.sh")
    log.info(f'Executing config.sh on instance {name}')
    exec_command(name, "bash /home/ubuntu/config.sh")
    log.info(f'Removing config.sh from instance {name}')
    exec_command(name, "rm /home/ubuntu/config.sh")
    log.info(f'Uploading cloudflared certificat to instance {name}')
    put_file(name, "~/.cloudflared/cert.pem", "~/.cloudflared/cert.pem")


def init_instance(image=DEFAULT_INSTANCE_IMAGE, cpu=DEFAULT_INSTANCE_VCPUS, memory=DEFAULT_INSTANCE_MEMORY, config=True):
    """
    Initializes a new instance

    Args:
        image (str): The image of the instance, default is "22.04"
        cpu (str): The number of CPUs, default is "1"
        memory (str): The amount of memory, default is "2G"
        config (bool): Configures the instance with multipass requirements, default is True
    Returns:
        str: The name of the instance

    Example:
        >>> init_instance()
            "instance_name"
    """
    log.info("Starting instance initialization")
    name = instance_name_gen()
    launch_instance(name, image, cpu, memory)
    if config:
        log.info(f'Configuring instance {name} with multipass requirements')
        install_prerequisites(name)
    return name


def check_server_virtualization():
    """
    Check if the server supports virtualization, has Multipass installed, and has network access

    Returns:
        bool: True if the server meets all requirements, False otherwise

    Example:
        >>> check_server_virtualization()
            True
    """
    log.info('Checking if the server meets all requirements')
    try:
        subprocess.run(["multipass", "--version"], check=True)
    except subprocess.CalledProcessError:
        log.error('Multipass is not installed')
        return False

    try:
        socket.create_connection(("www.google.com", 80))
    except OSError:
        log.error('No network access')
        return False

    return True