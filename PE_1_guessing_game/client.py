#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Client script that sends a guess to the server.

Usage: client.py

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-21
Version: v1
"""


import sys, Ice                                                                                 # Import the sys and Ice libraries (Ice runtime).
import NumberGuessingGame                                                                       # Import the NumberGuessingGame module (proxies and skeletons).
import argparse                                                                                 # Import the argparse library for cmd arguments.


def main() -> bool:
    """
    Main function.
    
    Returns:
        A boolean indicating the success of the process.
    """
    host = 'localhost'                                                                          # Set the default host.
    port = 10000                                                                                # Set the default port number.
    result = None                                                                               # Initialize the 'result' variable to None.
    print(f'Host: {host} (connecting port: {port})\n')                                          # Print the host and port number.

    with Ice.initialize(sys.argv) as communicator:                                              # Initialize the Ice run time and create a communicator.

        # Connect to the server.
        proxy = communicator.stringToProxy(                                                     # Create a proxy for the 'NumberGuessingGame' object, which can be communicated
            f'NumberGuessingGame:default -h {host} -p {port}'                                   # with via the host with the IP address or localhost using the specified
        )                                                                                       # port number and the default communication protocol.

        server = NumberGuessingGame.GamePrx.checkedCast(proxy)                                  # Cast the given 'proxy' to a 'Game' proxy and assign the resulting
        if not server:                                                                          # object to the variable 'server'. This allows communication with the
            raise RuntimeError('Invalid proxy')                                                 # remote 'Game' object via the 'server' object.

        # Start the game.
        while result != 'Correct':                                                              # Loop until the guess is correct.

            guess = int(input('Enter your guess from 1 to 100 (or 0 to quit): '))               # Ask the user for a guess.
            if guess == 0:                                                                      # Check if the guess is 0.
                print('\nQuitting the game.')
                return 0

            result = server.checkGuess(guess)                                                   # Call the functions on the 'server' object.
            print(result)                                                                       # Print the result of the guess.

        print('\nQuitting the game.')

    return 0


if __name__ == '__main__':
    sys.exit(main())                                                                            # Call the main function and exit with the returned status code.
