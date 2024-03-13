#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Server script that displays in the terminal the two numbers received,
calculates the result and returns it to the client.

Usage: server.py [-h] [--port PORT]

Pro calculator server script.

options:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  Port number. Use port 10000 (default) onwards.

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-13
Version: v1
"""


import sys, Ice                                                                                 # Import the sys and Ice libraries (Ice runtime).
import CalculatorPro                                                                            # Import the CalculatorPro module (proxies and skeletons).
import argparse                                                                                 # Import the argparse library for cmd arguments.


def get_args() -> argparse.Namespace:
    """
    Parse and retrieve command-line arguments.

    Returns:
        An 'argparse.Namespace' object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Pro calculator server script.')               # Parser creation and description.

    parser.add_argument('--port', '-p', type=int, default=10000,                                # Options.
                        help='Port number. Use port 10000 (default) onwards.')

    return parser.parse_args(sys.argv[1:])                                                      # Parse and return the arguments.


class AddSubServerI(CalculatorPro.Operations):                                                  # Define two classes that inherit from the 'Operations' class in the 'CalculatorPro' module.
    """
    Class that implements the 'Operations' interface.
    This class inherits from the 'Operations' class in the 'CalculatorPro' module.

    Methods:
        add(a, b, current=None): Method that adds two numbers.
        subtract(a, b, current=None): Method that subtracts two numbers.
    """
    def add(self, a, b, current=None):
        res = a + b
        print(f'{a} + {b} = {res}')
        return res
    def subtract(self, a, b, current=None):
        res = a - b
        print(f'{a} - {b} = {res}')
        return res


class MulDivServerI(CalculatorPro.Operations):
    """
    Class that implements the 'Operations' interface.
    This class inherits from the 'Operations' class in the 'CalculatorPro' module.

    Methods:
        multiply(a, b, current=None): Method that multiplies two numbers.
        divide(a, b, current=None): Method that divides two numbers.
    """
    def multiply(self, a, b, current=None):
        res = a * b
        print(f'{a} · {b} = {res}')
        return res
    def divide(self, a, b, current=None):
        try:
            res = a / b
        except ZeroDivisionError:
            print("Error: Division by zero!")
        print(f'{a} / {b} = {res}')
        return res


def main(args: argparse.Namespace) -> bool:
    """
    Main function.

    Args:
        args: An 'argparse.Namespace' object containing the parsed arguments.
    
    Returns:
        A boolean indicating the success of the process.
    """
    port = args.port                                                                            # Get the port number from the command line arguments.
    if isinstance(port, list):                                                                  # Preventing errors: If it is a list, take the item.
        port = port[0]

    print(f'Listening port: {port}')

    with Ice.initialize(sys.argv) as communicator:                                              # Initialize the Ice run time and create a communicator.

        adapter = communicator.createObjectAdapterWithEndpoints(                                # Create an object adapter with the name 'CalculatorProAdapter' and an
            'CalculatorProAdapter', f'default -p {port}'                                        # endpoint with the default protocol and the specified port number.
        )

        add_sub_servant = AddSubServerI()                                                       # Create the instances of the classes.
        mul_div_servant = MulDivServerI()

        add_sub_proxy = adapter.add(add_sub_servant,communicator.stringToIdentity('AddSub'))    # Add the servant instances to the adapter with each of the identities.
        mul_div_proxy = adapter.add(mul_div_servant, communicator.stringToIdentity('MulDiv'))

        adapter.activate()                                                                      # Activate the adapter to make the servant available for incoming requests.
        communicator.waitForShutdown()                                                          # Wait for the communicator to be destroyed.

    return 0


if __name__ == '__main__':
    args = get_args()                                                                           # Parse and retrieve command-line arguments.
    sys.exit(main(args))                                                                        # Call the main function and exit with the returned status code.