"""Server script that displays in the terminal the two numbers received,
   calculates the result and returns it to the client.

Usage: server.py [-h] [--port PORT]

Server script.

options:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  port number. Use port 10000 (default) onwards.

Author:
    A.J. Sanchez-Fernandez - 13/03/2023
"""


# Import the sys and Ice libraries.
import sys, Ice

# Import the Calculator module.
import Calculator

# Add a path to a custom argparse module.
sys.path.append('../')
from modules import custom_argparse


# Define a class that inherits from the 'Operations' class in the 'Calculator' module.
class OperationsI(Calculator.Operations):
    def add(self, a, b, current=None):
        res = a + b
        print(f'{a} + {b} = {res}')
        return res
    def subtract(self, a, b, current=None):
        res = a - b
        print(f'{a} - {b} = {res}')
        return res
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
    port = args.port

    # Print the port number.
    print(f'Listening port: {port}')

    # Initialize the Ice communicator.
    with Ice.initialize(sys.argv) as communicator:

        # Create an object adapter with the name 'BasicCalculator' and an
        # endpoint with the default protocol and the specified port number.
        adapter = communicator.createObjectAdapterWithEndpoints('BasicCalculatorAdapter',
                                                                f'default -p {port}')
    
        # Create an instance of the 'OperationsI' class.
        servant = OperationsI()
    
        # Add the 'servant' instance to the adapter with the identity 'BasicCalculator'.
        proxy = adapter.add(servant, communicator.stringToIdentity('BasicCalculator'))

        # Activate the adapter.
        adapter.activate()
    
        # Wait for the communicator to shut down.
        communicator.waitForShutdown()

    return 0

# Call the main function to execute the program.
if __name__ == '__main__':
    sys.exit(main())
