"""Client script that sends a text to a server.

Usage: client.py [-h] [--host HOST] [--port PORT] [--text]

Printer client script.

options:
  -h, --help            show this help message and exit
  --host HOST, -ht HOST
                        Communication via the host. Use localhost (default) or give an IP address (e.g., 192.168.1.140).
  --port PORT, -p PORT  Port number. Use port 10000 (default) onwards.
  --text, -t            Allows text to be entered via the terminal.

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
    parser = argparse.ArgumentParser(description='Printer client script.')                      # Parser creation and description.

    parser.add_argument('--host', '-ht', type=str, default='localhost',                         # Options.
                        help=('Communication via the host. Use localhost (default) '
                             'or give an IP address (e.g., 192.168.1.140).'))

    parser.add_argument('--port', '-p', type=int, default=10000,
                        help='Port number. Use port 10000 (default) onwards.')

    parser.add_argument('--text', '-t', action='store_true',
                        help='Allows text to be entered via the terminal.')

    return parser.parse_args(sys.argv[1:])                                                      # Parse and return the arguments.


def main(args: argparse.Namespace) -> bool:
    """
    Main function.

    Args:
        args: An 'argparse.Namespace' object containing the parsed arguments.
    
    Returns:
        A boolean indicating the success of the process.
    """
    if args.text:                                                                               # Get the text to be printed (if enabled).
        text = input('Enter the text to be sent to the printer: ')
    else:
        text = 'Hello world!'

    print(f'Host: {args.host} (connecting port: {args.port})')                                  # Print the host address and port number.

    with Ice.initialize(sys.argv) as communicator:                                              # Initialize the Ice run time and create a communicator.

        proxy = communicator.stringToProxy(                                                     # Create a proxy for the 'SimplePrinter' object, which can be communicated
            f'SimplePrinter:default -h {args.host} -p {args.port}'                              # with via the host with the IP address or localhost using the specified
        )                                                                                       # port number and the default communication protocol.

        server = Printer.OperationPrx.checkedCast(proxy)                                        # Cast the given 'proxy' to a 'Operation' proxy and assign the resulting
        if not server:                                                                          # object to the variable 'server'. This allows communication with the
            raise RuntimeError('Invalid proxy')                                                 # remote 'Operation' object via the 'server' object.

        server.printString(text)                                                                # Call the 'printString' method on the 'server' object, passing the 'text'.
        print(f'Text sent correctly to the printer!')

    return 0


if __name__ == '__main__':
    args = get_args()                                                                           # Parse and retrieve command-line arguments.
    sys.exit(main(args))
