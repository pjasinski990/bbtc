# BBTC Client

## Overview
This is a python implementation of Bluetooth Based Thread Commissioning client, based on Thread's TCAT (Thread Commissioning over Authenticated TLS) functionality.

## Installation
If you don't have poetry module installed (check with `poetry --version`), install it first using:
```bash
python3 -m pip install poetry
```

Then, enter the project directory (the one containing `pyproject.toml`) and install the dependencies:
```
poetry install
```

This will install all the required modules to a virtual environment, which can be used by calling `poetry run <COMMAND>` from the project directory.

## Usage
In order to connect to a TCAT device, enter the project directory and run:
```bash
poetry run python3 bbtc.py {<device specifier> | --scan}
```
where device specifier can be:
- `--name <NAME>` - name advertised by the device
- `--mac <ADDRESS>` - physical address of the device's Bluetooth interface
- `--uuid <SERVICE_UUID>` - UUID of a service that is advertised by the device

Using `--scan` option will scan for every TCAT device and display them in a list, to allow selection of the target.

For example:
```
poetry run python3 bbtc.py --name 'Thread BLE'
```

The application will connect to the first discovered, matching device and set up a secure TLS channel. The user is then presented with CLI.

## Commands
The application supports following interactive CLI commands:
- `help` - display available commands
- `commission` - commission the device with a predefined, hardcoded dataset
- `thread start` - enable Thread interface
- `thread stop` - disable Thread interface
- `hello` - send "hello world" application data and read the response
- `exit` - close the connection and exit
