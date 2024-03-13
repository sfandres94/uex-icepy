#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Server script that displays a received text in the terminal.

Usage: server.py [-h] [--port PORT]

Printer server script.

options:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  Port number. Use port 10000 (default) onwards.

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-10
Version: v1
"""


import sys, Ice                                                                                 # Import the sys and Ice libraries (Ice runtime).
import Printer                                                                                  # Import the Printer module (proxies and skeletons).
import argparse                                                                                 # Import the argparse library for cmd arguments.


def get_args() -> argparse.Namespace:
    """
    Parse and retrieve command-line arguments.

    Returns:
        An 'argparse.Namespace' object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Printer server script.')                      # Parser creation and description.

    parser.add_argument('--port', '-p', type=int, default=10000,                                # Options.
                        help='Port number. Use port 10000 (default) onwards.')

    return parser.parse_args(sys.argv[1:])                                                      # Parse and return the arguments.


class OperationI(Printer.Operation):                                                            # Define a class that inherits from the 'Operation' class in the 'Printer' module.
    """
    Class that implements the 'Operation' interface.
    This class inherits from the 'Operation' class in the 'Printer' module.

    Methods:
        printString(s, current=None): Method that prints the given string.
    """
    def printString(self, s, current=None):
        """Method that prints the given string."""
        print(s)


def main(args: argparse.Namespace) -> bool:
    """
    Main function.

    Args:
        args: An 'argparse.Namespace' object containing the parsed arguments.
    
    Returns:
        A boolean indicating the success of the process.
    """
    print(f'Listening port: {args.port}')                                                       # Print the host address and port number.

    with Ice.initialize(sys.argv) as communicator:                                              # Initialize the Ice run time and create a communicator.

        adapter = communicator.createObjectAdapterWithEndpoints(                                # Create an object adapter with the name 'SimplePrinterAdapter' and an    
            'SimplePrinterAdapter', f'default -p {args.port}'                                   # endpoint with the default protocol and the specified port number.
        )

        servant = OperationI()                                                                  # Create an instance of the 'OperationI' class.

        proxy = adapter.add(servant, communicator.stringToIdentity('SimplePrinter'))            # Add the 'servant' instance to the adapter with the identity 'SimplePrinter' and get the proxy.

        adapter.activate()                                                                      # Activate the adapter to make the servant available for incoming requests.
        communicator.waitForShutdown()                                                          # Wait for the communicator to be destroyed.

    return 0


if __name__ == '__main__':
    args = get_args()                                                                           # Parse and retrieve command-line arguments.
    sys.exit(main(args))                                                                        # Call the main function and exit with the returned status code.
