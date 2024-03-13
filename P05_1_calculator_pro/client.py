#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Client script that sends two numbers to two servers and displays
the result received in the terminal. Any server can act as
the add or mul server simply by interchanging the port numbers.

Usage: 

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-13
Version: v1
"""


import sys, Ice                                                                                 # Import the sys and Ice libraries (Ice runtime).
import CalculatorPro                                                                            # Import the CalculatorPro module (proxies and skeletons).
import argparse                                                                                 # Import the argparse library for cmd arguments.


# Main function.
def main():

    # Get command line arguments using the custom_argparse module.
    args = custom_argparse.get_args(description='Client script.',
                                    role='client',
                                    example='calculator',
                                    argv=sys.argv)

    # Get the hostname, port number and numbers from the command line arguments.
    # Preventing errors: If it is not a list (not two hostnames), then duplicate
    # the names; if it is a list but with only one item, repeate the item twice.
    host = args.host
    if not isinstance(host, list):
        host = (host, host)
    elif isinstance(host, list) and len(host)==1:
        host = (host[0], host[0])

    port = args.port
    if not isinstance(port, list):
        port = (port, port+1)
    elif isinstance(port, list) and len(port)==1:
        port = (port[0], port[0]+1)

    num1 = args.num1
    num2 = args.num2
    
    if num1==None or num2==None:
        num1 = float(input('Enter the first number: '))
        num2 = float(input('Enter the second number: '))
 
    # Print the host address and port number.
    print(f'Hosts: {host} (connecting port/s: {port})')

    # Initialize the Ice communicator.
    with Ice.initialize(sys.argv) as communicator:

        # Create two proxies, which can be communicated with via
        # the host with the IP address or localhost using the specified
        # port number and the default communication protocol.
        add_sub_proxy = communicator.stringToProxy(f'AddSub:default -h {host[0]} -p {port[0]}')
        mul_div_proxy = communicator.stringToProxy(f'MulDiv:default -h {host[1]} -p {port[1]}')

        # Cast the given 'proxy' to a 'Operations' proxy and assign the resulting object to the variable
        # 'server'. This allows communication with the remote 'Operations' object via the server objects.
        add_sub_server = CalculatorPro.OperationsPrx.checkedCast(add_sub_proxy)
        mul_div_server = CalculatorPro.OperationsPrx.checkedCast(mul_div_proxy)
        if not add_sub_server or not mul_div_server:
            raise RuntimeError('Invalid proxy')
    
        # Call the functions on the server objects.
        print(f'Result of add.: {add_sub_server.add(num1, num2)}')
        print(f'Result of sub.: {add_sub_server.subtract(num1, num2)}')
        print(f'Result of mul.: {mul_div_server.multiply(num1, num2)}')
        print(f'Result of div.: {mul_div_server.divide(num1, num2)}')

    return 0

# Call the main function to execute the program.
if __name__ == '__main__':
    sys.exit(main())
