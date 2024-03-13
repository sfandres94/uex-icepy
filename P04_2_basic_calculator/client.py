"""Client script that sends two numbers to a server
   and displays the result received in the terminal.

Usage: client.py [-h] [--port PORT] [--host HOST] [--num1 NUM1] [--num2 NUM2]

Client script.

options:
  -h, --help             show this help message and exit
  --port PORT, -p PORT   port number. Use port 10000 (default) onwards.
  --host HOST, -ht HOST  communication via the host. Use localhost (default) or give an IP address (e.g., 192.168.1.140).
  --num1 NUM1, -n1 NUM1  first number.
  --num2 NUM2, -n2 NUM2  second number.

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


# Main function.
def main():

    # Get command line arguments using the custom_argparse module.
    args = custom_argparse.get_args(description='Client script.',
                                    role='client',
                                    example='calculator',
                                    argv=sys.argv)

    # Get the hostname, port number and numbers from the command line arguments.
    host = args.host
    port = args.port
    num1 = args.num1
    num2 = args.num2
    
    if num1==None or num2==None:
        num1 = float(input('Enter the first number: '))
        num2 = float(input('Enter the second number: '))
 
    # Print the host address and port number.
    print(f'Host: {host} (connecting port: {port})')

    # Initialize the Ice communicator.
    with Ice.initialize(sys.argv) as communicator:

        # Create a proxy for the 'BasicCalculator' object, which can be communicated
        # with via the host with the IP address or localhost using the specified
        # port number and the default communication protocol.
        proxy = communicator.stringToProxy(f'BasicCalculator:default -h {host} -p {port}')

        # Cast the given 'proxy' to a 'Operations' proxy and assign the resulting object to the variable
        # 'server'. This allows communication with the remote 'Operations' object via the 'server' object.
        server = Calculator.OperationsPrx.checkedCast(proxy)
        if not server:
            raise RuntimeError('Invalid proxy')
    
        # Call the functions on the 'server' object.
        print(f'Result of add.: {server.add(num1, num2)}')
        print(f'Result of sub.: {server.subtract(num1, num2)}')
        print(f'Result of mul.: {server.multiply(num1, num2)}')
        print(f'Result of div.: {server.divide(num1, num2)}')

    return 0

# Call the main function to execute the program.
if __name__ == '__main__':
    sys.exit(main())
