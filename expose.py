import argparse
import json
import os
import subprocess
import socket
import re
import socket
import yaml
import psutil


STATUS_FILE = 'port_status'
HOME_DIR = os.path.expanduser('~')
DOMAIN_URL = 'skead.fr'

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def save_status(status):
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f)

def start(port):
    print(f'Starting service on port {port}...', end=' ')
    status = load_status()
    status[port] = 'started'
    save_status(status)

    tunnel_name = f'{socket.gethostname()}-{port}'
    print(f'Creating tunnel {tunnel_name}...')
    result = subprocess.run(['cloudflared', 'tunnel', 'create', tunnel_name], capture_output=True, text=True, check=True)

    match = re.search(rf'{HOME_DIR}/.cloudflared/([a-f0-9-]+\.json)', result.stdout)
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
        'credentials-file': f'{HOME_DIR}/.cloudflared/{json_file_name}'
    }
    with open(f'{HOME_DIR}/.cloudflared/{tunnel_name}.yml', 'w') as f:
        yaml.dump(config, f)

    subprocess.run(['cloudflared', 'tunnel', 'route', 'dns', tunnel_name, f'{tunnel_name}.{DOMAIN_URL}'], check=True)

    subprocess.Popen(['cloudflared', 'tunnel', '--config', f'{HOME_DIR}/.cloudflared/{tunnel_name}.yml', 'run', tunnel_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\033[92m[OK]\033[0m")

def stop(port):
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
    print('Listing all services...')
    status = load_status()
    for port, state in status.items():
        print(f'Service on port {port} is {state}')

def restart(port):
    print(f'Restarting service on port {port}...')
    stop(port)
    start(port)

def delete(port):
    print(f'Deleting service on port {port}...', end=' ')

    tunnel_name = f'{socket.gethostname()}-{port}'
    stop(port)

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'cloudflared' in proc.info['name'] and tunnel_name in proc.info['cmdline']:
            proc.terminate()
            break

    config_file = f'{HOME_DIR}/.cloudflared/{tunnel_name}.yml'
    if os.path.exists(config_file):
        os.remove(config_file)
    subprocess.run(['cloudflared', 'tunnel', 'cleanup', tunnel_name], check=True)
    subprocess.run(['cloudflared', 'tunnel', 'route', 'delete', f'{tunnel_name}.skead.fr'], check=True)
    subprocess.run(['cloudflared', 'tunnel', 'delete', tunnel_name], check=True)

    status = load_status()
    status[port] = 'deleted'
    save_status(status)
    print("\033[92m[OK]\033[0m")

def main():
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