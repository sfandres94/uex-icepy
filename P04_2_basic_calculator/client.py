#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Client script that sends two numbers to a server
and displays the result received in the terminal.

Usage: client.py [-h] [--host HOST] [--port PORT]

Basic calculator client script.

options:
  -h, --help            show this help message and exit
  --host HOST, -ht HOST
                        Communication via the host. Use localhost (default) or give an IP address (e.g., 192.168.1.140).
  --port PORT, -p PORT  Port number. Use port 10000 (default) onwards.

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-13
Version: v1
"""


import sys, Ice                                                                                 # Import the sys and Ice libraries (Ice runtime).
import Calculator                                                                               # Import the Calculator module (proxies and skeletons).
import argparse                                                                                 # Import the argparse library for cmd arguments.


def get_args() -> argparse.Namespace:
    """
    Parse and retrieve command-line arguments.

    Returns:
        An 'argparse.Namespace' object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Basic calculator client script.')             # Parser creation and description.

    parser.add_argument('--host', '-ht', type=str, default='localhost',                         # Options.
                        help=('Communication via the host. Use localhost (default) '
                             'or give an IP address (e.g., 192.168.1.140).'))

    parser.add_argument('--port', '-p', type=int, default=10000,
                        help='Port number. Use port 10000 (default) onwards.')

    return parser.parse_args(sys.argv[1:])                                                      # Parse and return the arguments.


def main(args: argparse.Namespace) -> bool:
    """
    Main function.

    Args:
        args: An 'argparse.Namespace' object containing the parsed arguments.
    
    Returns:
        A boolean indicating the success of the process.
    """
    number1 = float(input('Enter the first number: '))
    number2 = float(input('Enter the second number: '))
 
    print(f'Numbers: {number1} and {number2}')                                                  # Print the numbers to be sent to the server.
    print(f'Host: {args.host} (connecting port: {args.port})')                                  # Print the host address and port number.

    with Ice.initialize(sys.argv) as communicator:                                              # Initialize the Ice run time and create a communicator.

        proxy = communicator.stringToProxy(                                                     # Create a proxy for the 'BasicCalculator' object, which can be communicated
            f'BasicCalculator:default -h {args.host} -p {args.port}'                            # with via the host with the IP address or localhost using the specified
        )                                                                                       # port number and the default communication protocol.

        server = Calculator.OperationsPrx.checkedCast(proxy)                                    # Cast the given 'proxy' to a 'Operations' proxy and assign the resulting
        if not server:                                                                          # object to the variable 'server'. This allows communication with the
            raise RuntimeError('Invalid proxy')                                                 # remote 'Operations' object via the 'server' object.

        print(f'Result of add.: {server.add(number1, number2)}')                                # Call the methods on the 'server' object, passing the 'number1' and 'number2'.
        print(f'Result of sub.: {server.subtract(number1, number2)}')                             
        print(f'Result of mul.: {server.multiply(number1, number2)}')
        print(f'Result of div.: {server.divide(number1, number2)}')

    return 0


if __name__ == '__main__':
    args = get_args()                                                                           # Parse and retrieve command-line arguments.
    sys.exit(main(args))                                                                        # Call the main function and exit with the returned status code.
