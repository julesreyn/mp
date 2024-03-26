##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## multipass library
## @julesreyn
##

from taker_lib import *
import logging
import datetime

DEFAULT_INSTANCE_IMAGE = "22.04" # available options: 20.04, 22.04, 23.10, daily:24.04, docker, jellyfin, core, core18, core20, core22  -> search new image with "multipass find"
DEFAULT_INSTANCE_VCPUS = "1" # available options: 1, 2, 4, 6
DEFAULT_INSTANCE_MEMORY = "2G" # available options: 512M, 1G, 2G, 4G, 8G

log = logging.getLogger(__name__)


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
    put_file(name, "./setup_tools/config.sh", "config.sh")
    put_file(name, "./setup_tools/update-motd.d/00-header", "00-header")
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
    upload_config(name)
    exec_command(name, "bash /home/ubuntu/config.sh")
    exec_command(name, "rm /home/ubuntu/config.sh")
    put_file(name, "~/.cloudflared/cert.pem", "~/.cloudflared/cert.pem")



def init_instance(image=DEFAULT_INSTANCE_IMAGE, cpu=DEFAULT_INSTANCE_VCPUS, memory=DEFAULT_INSTANCE_MEMORY):
    """
    Initializes a new instance

    Args:
        image (str): The image of the instance
        cpu (str): The number of CPUs
        memory (str): The amount of memory

    Returns:
        str: The name of the instance

    Example:
        >>> init_instance()
            "instance_name"
    """
    name = instance_name_gen()
    launch_instance(name, image, cpu, memory)
    install_prerequisites(name)
    return name



if __name__ == "__main__":
    logging.basicConfig(filename=f"logs/instances/init-vm-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    log.info("Starting instance initialization")
    init_instance()