##
## Multipass Library - 2024
## mp [Ubuntu:22.04]
## File description:
## multipass expose command to expose services and ports
## @julesreyn
##

import argparse
import json
import subprocess
import socket
import re
from pathlib import Path
import yaml
import psutil
import shelve
from tabulate import tabulate
import secrets
import string

STATUS_FILE = 'port_status'
HOME_DIR = Path.home()
CLOUDFLARED_DIR = HOME_DIR / '.cloudflared'
DOMAIN_URL = 'skead.fr'


def load_status():
    """
    Load the status of all services from a file.

    Returns:
        dict: A dictionary mapping port numbers to service statuses.

    This function loads the status of all services from a file named 'port_status' in the current directory.
    If the file does not exist, an empty dictionary is returned.
    """
    status = {}
    with shelve.open(STATUS_FILE) as db:
        status = {int(k): v for k, v in db.items()}
    return status


def save_status(status):
    """
    Save the status of all services to a file.

    Args:
        status (dict): A dictionary mapping port numbers to service statuses.

    This function saves the status of all services to a file named 'port_status' in the current directory.
    """
    with shelve.open(STATUS_FILE) as db:
        db.clear()
        db.update({str(k): v for k, v in status.items()})


def get_service_name(port):
    """
    Get the name of a service running on a specified port using /etc/services file.

    Args:
        port (int): The port number on which the service is running.

    Returns:
        str: The name of the service running on the specified port.

    This function runs a command to determine the name of the service running on the specified port.
    The output of the command is returned as a string.
    """
    result = subprocess.run(['grep', '-w', f'{port}/tcp', '/etc/services'], capture_output=True, text=True)
    if result.stdout:
        return result.stdout.split()[0]

    result = subprocess.run(['grep', '-w', f'{port}/udp', '/etc/services'], capture_output=True, text=True)
    if result.stdout:
        return result.stdout.split()[0]

    return None


def start(port, protocol='http'):
    """
    Start a service on a specified port and create a tunnel for it.

    Args:
        port (int): The port number on which to start the service.

    This function performs the following steps:
    1. Prints a message indicating that the service is starting.
    2. Loads the current status of all services.
    3. Sets the status of the specified service to 'started' and saves the status.
    4. Creates a tunnel name based on the hostname and port number.
    5. Runs a command to create a tunnel using the 'cloudflared' tool.
    6. Searches the output of the command for a JSON file name.
    7. If a JSON file name is found, it is used to create a configuration for the tunnel.
    8. The configuration is saved to a YAML file.
    9. Runs a command to route DNS traffic through the tunnel.
    10. Runs a command to start the tunnel.
    11. Prints a message indicating that the service has started.
    """
    print(f'Starting service on port {port}...', end=' ')
    status = load_status()
    tunnel_name = f'{socket.gethostname()}-{port}'
    print(f'Creating tunnel {tunnel_name}...')
    result = subprocess.run(['cloudflared', 'tunnel', 'create', tunnel_name], capture_output=True, text=True, check=True)
    match = re.search(rf'{CLOUDFLARED_DIR}/([a-f0-9-]+\.json)', result.stdout)
    if match:
        json_file_name = match.group(1)
    else:
        print('Could not find JSON file name in output')
        return

    hostname = socket.gethostname()
    random_string = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    tunnel_name_port = f'{hostname}-{port}-{random_string}'
    config = {
        'url': f'{protocol}://localhost:{port}',
        'tunnel': tunnel_name,
        'credentials-file': str(CLOUDFLARED_DIR / json_file_name)
    }
    with (CLOUDFLARED_DIR / f'{tunnel_name_port}.yml').open('w') as f:
        yaml.dump(config, f)

    subprocess.run(['cloudflared', 'tunnel', 'route', 'dns', tunnel_name, f'{tunnel_name_port}.{DOMAIN_URL}'], check=True)
    subprocess.Popen(['cloudflared', 'tunnel', '--config', str(CLOUDFLARED_DIR / f'{tunnel_name_port}.yml'), 'run', tunnel_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    service_name = get_service_name(port)
    status[port] = {
        'status': 'started',
        'url': f'{tunnel_name_port}.{DOMAIN_URL}',
        'service': service_name
    }
    save_status(status)
    print("\033[92m[OK]\033[0m")



def stop(port):
    """
    Stop a service on a specified port and delete the tunnel for it.

    Args:
        port (int): The port number on which to stop the service.

    This function performs the following steps:
    1. Prints a message indicating that the service is stopping.
    2. Loads the current status of all services.
    3. Sets the status of the specified service to 'stopped' and saves the status.
    4. Creates a tunnel name based on the hostname and port number.
    5. Searches for a 'cloudflared' process with the tunnel name in its command line.
    6. Terminates the process if found.
    7. Prints a message indicating that the service has stopped.
    """
    print(f'Stopping service on port {port}...', end=' ')
    tunnel_name = f'{socket.gethostname()}-{port}'
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'cloudflared' in proc.info['name'] and tunnel_name in proc.info['cmdline']:
            proc.terminate()
            break

    status = load_status()
    if port in status:
        status[port]['status'] = 'stopped'
    else:
        status[port] = {'status': 'stopped'}
    save_status(status)
    print("\033[92m[OK]\033[0m")



def list_services():
    """
    List all services and their statuses.

    This function performs the following steps:
    1. Prints a message indicating that all services are being listed.
    2. Loads the current status of all services.
    3. If no services are running, prints "No port running".
    4. Otherwise, prints the status of each service in a table format.
    """
    status = load_status()
    if not status:
        print("No port running, use 'expose start <port>' to start a port redirection or use the 'expose -h' command to see the help")
    else:
        table = [["Port", "Service", "URL", "Status"]]
        status_order = {'started': 0, 'stopped': 1, 'deleted': 2}
        sorted_status = sorted(status.items(), key=lambda item: status_order.get(item[1]['status'], 3))
        for port, state in sorted_status:
            table.append([port, state['service'], state['url'], state['status']])
        print(tabulate(table, headers="firstrow", tablefmt="pipe"))


def restart(port):
    """
    Restart a service on a specified port.

    Args:
        port (int): The port number on which to restart the service.

    This function performs the following steps:
    1. Prints a message indicating that the service is restarting.
    2. Stops the service on the specified port.
    3. Starts the service on the specified port.
    """
    print(f'Restarting service on port {port}...')
    stop(port)
    start(port)



def delete(port):
    """
    Delete a service on a specified port and remove the tunnel for it.

    Args:
        port (int): The port number on which to delete the service.

    This function performs the following steps:
    1. Prints a message indicating that the service is being deleted.
    2. Deletes the service on the specified port.
    3. Searches for a 'cloudflared' process with the tunnel name in its command line.
    4. Terminates the process if found.
    5. Deletes the configuration file for the tunnel.
    6. Runs a command to clean up the tunnel.
    7. Runs a command to delete the route for the tunnel.
    8. Runs a command to delete the tunnel.
    9. Prints a message indicating that the service has been deleted.
    """
    print(f'Deleting service on port {port}...', end=' ')
    tunnel_name = f'{socket.gethostname()}-{port}'
    stop(port)
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'cloudflared' in proc.info['name'] and tunnel_name in proc.info['cmdline']:
            proc.terminate()
            break

    config_file = CLOUDFLARED_DIR / f'{tunnel_name}.yml'
    if config_file.exists():
        config_file.unlink()
    subprocess.run(['cloudflared', 'tunnel', 'cleanup', tunnel_name], check=True)
    subprocess.run(['cloudflared', 'tunnel', 'delete', tunnel_name], check=True)

    status = load_status()
    if port in status:
        status[port]['status'] = 'deleted'
    else:
        status[port] = {'status': 'deleted'}
    save_status(status)
    print("\033[92m[OK]\033[0m")


def get_tunnels():
    """
    Get all tunnels.

    Returns:
        list: A list of URLs for all tunnels.

    This function performs the following steps:
    1. Loads the current status of all services.
    2. If no services are running, returns an empty list.
    3. Otherwise, appends the URL of each service to a list.
    4. Returns the list of URLs.
    """
    tunnels = []
    status = load_status()
    for port, state in status.items():
        tunnels.append(state['url'])
    return tunnels


def stop_all_tunnels():
    """
    Stop all active tunnels.

    This function performs the following steps:
    1. Loads the current status of all services.
    2. For each service, if the service is running, stops the service.
    """
    status = load_status()
    for port, state in status.items():
        if state['status'] == 'started':
            stop(port)


def print_help(parser):
    parser.print_help()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Manage services.')
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    commands = {
        'start': 'Start the URL redirection from a specified port.',
        'stop': 'Stop the URL redirection from a specified port.',
        'list': 'List all services, their statuses, and their URLs.',
        'restart': 'Restart the URL redirection from a specified port.',
        'delete': 'Delete the exposed URL from a specified port.'
    }

    parsers = {command: subparsers.add_parser(command, help=description) for command, description in commands.items()}

    for command in ['start', 'stop', 'restart', 'delete']:
        parsers[command].add_argument('port', type=int, help='The port number on which to perform the operation.')

    return parser, parser.parse_args()


def main():
    parser, args = parse_arguments()

    command_to_function = {
        'start': start,
        'stop': stop,
        'list': list_services,
        'restart': restart,
        'delete': delete
    }

    if args.command in command_to_function:
        if args.command in ['start', 'stop', 'restart', 'delete']:
            command_to_function[args.command](args.port)
        elif args.command == 'list':
            command_to_function[args.command]()
    else:
        print_help(parser)

if __name__ == '__main__':
    main()


## TODO ##
## if port stop, restart it
## get the archive of all port create to delete cname after
## list port deleted