import argparse
import json
import subprocess
import socket
import re
from pathlib import Path
import yaml
import psutil



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

    status_file = Path(STATUS_FILE)
    if status_file.exists():
        with status_file.open() as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        return {}



def save_status(status):
    """
    Save the status of all services to a file.

    Args:
        status (dict): A dictionary mapping port numbers to service statuses.

    This function saves the status of all services to a file named 'port_status' in the current directory.
    """

    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f)



def start(port):
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
    status[port] = 'started'
    save_status(status)

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
    tunnel_name = f'{hostname}_{port}'

    config = {
        'url': f'http://localhost:{port}',
        'tunnel': tunnel_name,
        'credentials-file': str(CLOUDFLARED_DIR / json_file_name)
    }
    with (CLOUDFLARED_DIR / f'{tunnel_name}.yml').open('w') as f:
        yaml.dump(config, f)

    subprocess.run(['cloudflared', 'tunnel', 'route', 'dns', tunnel_name, f'{tunnel_name}.{DOMAIN_URL}'], check=True)

    subprocess.Popen(['cloudflared', 'tunnel', '--config', str(CLOUDFLARED_DIR / f'{tunnel_name}.yml'), 'run', tunnel_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
    status[port] = 'stopped'
    save_status(status)
    print("\033[92m[OK]\033[0m")



def list_services():
    """
    List all services and their statuses.

    This function performs the following steps:
    1. Prints a message indicating that all services are being listed.
    2. Loads the current status of all services.
    3. Prints the status of each service.
    """

    print('Listing all services...')
    status = load_status()
    for port, state in status.items():
        print(f'Service on port {port} is {state}')



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
    subprocess.run(['cloudflared', 'tunnel', 'route', 'delete', f'{tunnel_name}.{DOMAIN_URL}'], check=True)
    subprocess.run(['cloudflared', 'tunnel', 'delete', tunnel_name], check=True)

    status = load_status()
    status[port] = 'deleted'
    save_status(status)
    print("\033[92m[OK]\033[0m")



def main():
    """
    Parse command-line arguments and execute the corresponding command.

    This function parses the command-line arguments using the 'argparse' module and executes the corresponding command.
    The available commands are :

    - start: Start a service on a specified port.
    - stop: Stop a service on a specified port.
    - list: List all services and their statuses.
    - restart: Restart a service on a specified port.

    Each command takes a port number as an argument.
    """

    parser = argparse.ArgumentParser(description='Manage services.')
    subparsers = parser.add_subparsers(dest='command')

    start_parser = subparsers.add_parser('start')
    start_parser.add_argument('port', type=int)

    stop_parser = subparsers.add_parser('stop')
    stop_parser.add_argument('port', type=int)

    list_parser = subparsers.add_parser('list')

    restart_parser = subparsers.add_parser('restart')
    restart_parser.add_argument('port', type=int)

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('port', type=int)

    args = parser.parse_args()

    if args.command == 'start':
        start(args.port)
    elif args.command == 'stop':
        stop(args.port)
    elif args.command == 'list':
        list_services()
    elif args.command == 'restart':
        restart(args.port)
    elif args.command == 'delete':
        delete(args.port)

if __name__ == '__main__':
    main()