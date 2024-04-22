##
## Multipass Library - 2024
## mp [Ubuntu:22.04]
## File description:
## multipass instance library for multipass file operations
## @julesreyn
##

from mp.logger import logger
import subprocess
import os
import logging

log = logging.getLogger(__name__)


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
    log.info(f'Transferring file to instance {name}: {source} -> {destination}')
    if not os.path.exists(source):
        logger(instance=name, error=f"warning: source file {source} does not exist.", status="warning")
        return False
    result = subprocess.run(["multipass", "transfer", source, f"{name}:{destination}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'File transferred to instance {name}: {source} -> {destination}')
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
    log.info(f'Transferring file from instance {name}: {source} -> {destination}')
    result = subprocess.run(["multipass", "transfer", f"{name}:{source}", destination], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'File transferred from instance {name}: {source} -> {destination}')
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
    log.info(f'Mounting directory to instance {name}: {source} -> {destination}')
    result = subprocess.run(["multipass", "mount", source, f"{name}:{destination}"], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'Directory mounted to instance {name}: {source} -> {destination}')
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
    log.info(f'Unmounting directory from instance {name}')
    result = subprocess.run(["multipass", "unmount", name], capture_output=True, text=True)
    if result.returncode != 0:
        logger(instance=name, error=result.stderr)
    log.info(f'Directory unmounted from instance {name}')
    return result.returncode == 0