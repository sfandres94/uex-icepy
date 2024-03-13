#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Server script that displays in the terminal the two numbers received,
calculates the result and returns it to the client.

Usage: 

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-13
Version: v1
"""


import sys, Ice                                                                                 # Import the sys and Ice libraries (Ice runtime).
import CalculatorPro                                                                            # Import the CalculatorPro module (proxies and skeletons).
import argparse                                                                                 # Import the argparse library for cmd arguments.


# Define two classes that inherit from the 'Operations' class in the 'CalculatorPro' module.
class AddSubServerI(CalculatorPro.Operations):
    def add(self, a, b, current=None):
        res = a + b
        print(f'{a} + {b} = {res}')
        return res
    def subtract(self, a, b, current=None):
        res = a - b
        print(f'{a} - {b} = {res}')
        return res

class MulDivServerI(CalculatorPro.Operations):
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


# Main function.
def main():

    # Get command line arguments using the custom_argparse module.
    args = custom_argparse.get_args(description='Server script.',
                                    role='server',
                                    example='calculator',
                                    argv=sys.argv)

    # Get the port number from the command line arguments.
    # Preventing errors: If it is a list, take the item.
    port = args.port
    if isinstance(port, list):
        port = port[0]

    # Print the port number.
    print(f'Listening port: {port}')

    # Initialize the Ice communicator.
    with Ice.initialize(sys.argv) as communicator:

        # Create an object adapter with the name 'CalculatorProAdapter' and an
        # endpoint with the default protocol and the specified port number.
        adapter = communicator.createObjectAdapterWithEndpoints('CalculatorProAdapter',
                                                                f'default -p {port}')
    
        # Create the instances of the classes.
        add_sub_servant = AddSubServerI()
        mul_div_servant = MulDivServerI()

        # Add the servant instances to the adapter with each of the identities.
        add_sub_proxy = adapter.add(add_sub_servant, communicator.stringToIdentity('AddSub'))
        mul_div_proxy = adapter.add(mul_div_servant, communicator.stringToIdentity('MulDiv'))

        # Activate the adapter.
        adapter.activate()
    
        # Wait for the communicator to shut down.
        communicator.waitForShutdown()

    return 0

# Call the main function to execute the program.
if __name__ == '__main__':
    sys.exit(main())
