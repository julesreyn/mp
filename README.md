# Conseil Junior Taker - 2024

This project provides a library for managing Ubuntu instances using Multipass.

## Features

- Generate unique instance names
- Launch new instances with specified parameters
- Upload configuration files to instances
- Install prerequisites on instances
- Initialize new instances with default or specified parameters

## Usage

The main entry point of the application is the `init_instance` function in `init-vm.py`. This function initializes a new instance with the specified or default parameters.

Here's an example of how to use it:

```shell
python3 init-vm.py
```

If you want to use the library in your own code, you can import the `init_instance` function and call it like this:

```python
from init-vm import init_instance

# Initialize a new instance with default parameters
init_instance()
```

## Configuration

You can configure the default parameters for new instances by modifying the following constants in init-vm.py:

DEFAULT_INSTANCE_IMAGE: The image of the instance (default: "22.04")
DEFAULT_INSTANCE_VCPUS: The number of CPUs (default: "1")
DEFAULT_INSTANCE_MEMORY: The amount of memory (default: "2G")

## Logging

The application logs its activity to a file in the logs/instances directory. The log file is named init-vm-<timestamp>.log, where <timestamp> is the date and time when the application was started.

The logs are also sended to Sysadmin's discord channel with the logger function.
This function can report multiple levels of logs: INFO, WARNING, ERROR, CRITICAL.

All logs are sended to the discord channel, but only the WARNING, ERROR and CRITICAL logs are sended to the sysadmin's discord channel.