#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Client script that sends two numbers to two servers and displays
the result received in the terminal. Any server can act as
the add or mul server simply by interchanging the port numbers.

Usage: client.py [-h] [--host HOST [HOST ...]] [--port PORT [PORT ...]] [--number1 NUMBER1] [--number2 NUMBER2]

Pro calculator client script.

options:
  -h, --help            show this help message and exit
  --host HOST [HOST ...], -ht HOST [HOST ...]
                        Communication via the host. Use localhost (default) or give an IP address (e.g., 192.168.1.140).
  --port PORT [PORT ...], -p PORT [PORT ...]
                        Port number. Use port 10000 (default) onwards.
  --number1 NUMBER1, -n1 NUMBER1
                        First number to be sent to the server.
  --number2 NUMBER2, -n2 NUMBER2
                        Second number to be sent to the server.

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
    parser = argparse.ArgumentParser(description='Pro calculator client script.')               # Parser creation and description.

    parser.add_argument('--host', '-ht', nargs='+', type=str, default='localhost',              # Options.
                        help=('Communication via the host. Use localhost (default) '
                             'or give an IP address (e.g., 192.168.1.140).'))

    parser.add_argument('--port', '-p', nargs='+', type=int, default=10000,
                        help='Port number. Use port 10000 (default) onwards.')

    parser.add_argument('--number1', '-n1', type=float, default=None,
                        help='First number to be sent to the server.')

    parser.add_argument('--number2', '-n2', type=float, default=None,
                        help='Second number to be sent to the server.')

    return parser.parse_args(sys.argv[1:])                                                      # Parse and return the arguments.


def main(args: argparse.Namespace) -> bool:
    """
    Main function.

    Args:
        args: An 'argparse.Namespace' object containing the parsed arguments.
    
    Returns:
        A boolean indicating the success of the process.
    """
    host = args.host                                                                            # Get the hostname, port number and numbers from the command line arguments.
    if not isinstance(host, list):                                                              # Preventing errors: If it is not a list (not two hostnames), then duplicate
        host = (host, host)                                                                     # the names; if it is a list but with only one item, repeate the item twice.
    elif isinstance(host, list) and len(host)==1:
        host = (host[0], host[0])

    port = args.port
    if not isinstance(port, list):
        port = (port, port+1)
    elif isinstance(port, list) and len(port)==1:
        port = (port[0], port[0]+1)

    if not args.number1 or not args.number2:                                                    # If the numbers are not given, ask for them.
        args.number1 = float(input('Enter the first number: '))
        args.number2 = float(input('Enter the second number: '))

    print(f'Numbers: {args.number1} and {args.number2}')                                        # Print the numbers to be sent to the server.
    print(f'Hosts: {host} (connecting port/s: {port})')                                         # Print the host address and port number.

    with Ice.initialize(sys.argv) as communicator:                                              # Initialize the Ice run time and create a communicator.

        add_sub_proxy = communicator.stringToProxy(                                             # Create two proxies, which can be communicated with via
            f'AddSub:default -h {host[0]} -p {port[0]}'                                         # the host with the IP address or localhost using the specified
        )                                                                                       # port number and the default communication protocol.
        mul_div_proxy = communicator.stringToProxy(
            f'MulDiv:default -h {host[1]} -p {port[1]}'
        )

        add_sub_server = CalculatorPro.OperationsPrx.checkedCast(add_sub_proxy)                 # Cast the given 'proxy' to a 'Operations' proxy and assign the resulting object to the variables.
        mul_div_server = CalculatorPro.OperationsPrx.checkedCast(mul_div_proxy)                 # This allows communication with the remote 'Operations' object via the server objects.
        if not add_sub_server or not mul_div_server:
            raise RuntimeError('Invalid proxy')
    
        print(f'Result of add.: {add_sub_server.add(args.number1, args.number2)}')              # Call the functions on the server objects.
        print(f'Result of sub.: {add_sub_server.subtract(args.number1, args.number2)}')
        print(f'Result of mul.: {mul_div_server.multiply(args.number1, args.number2)}')
        print(f'Result of div.: {mul_div_server.divide(args.number1, args.number2)}')

    return 0


if __name__ == '__main__':
    args = get_args()                                                                           # Parse and retrieve command-line arguments.
    sys.exit(main(args))                                                                        # Call the main function and exit with the returned status code.
