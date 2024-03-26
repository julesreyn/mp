##
## Conseil Junior Taker - 2024
## mp [Ubuntu:22.04]
## File description:
## taker instance library for taker instance initialization
## @julesreyn
##

from taker_lib.cmd.instance_operations import instance_name_gen, exec_command
from taker_lib.cmd.instance_operations import launch_instance
from taker_lib.cmd.file_operations import put_file
import	logging

log = logging.getLogger(__name__)

DEFAULT_INSTANCE_IMAGE = "22.04" # available options: 20.04, 22.04, 23.10, daily:24.04, docker, jellyfin, core, core18, core20, core22  -> search new image with "multipass find"
DEFAULT_INSTANCE_VCPUS = "1" # available options: 1, 2, 4, 6
DEFAULT_INSTANCE_MEMORY = "2G" # available options: 512M, 1G, 2G, 4G, 8G

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
    exec_command(name, "chmod +x /ome/ubuntu/config.sh")
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
        config (bool): Whether to configure the instance after launching, default is True

    Returns:
        str: The name of the instance

    Example:
        >>> init_instance()
            "instance_name"
    """
    name = instance_name_gen()
    launch_instance(name, image, cpu, memory)
    if config:
        log.info(f'Configuring instance {name} with Taker requirements')
        install_prerequisites(name)
    return name