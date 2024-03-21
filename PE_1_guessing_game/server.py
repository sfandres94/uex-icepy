#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Server script that compares the received number with the correct one.

Usage: server.py

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-21
Version: v1
"""


import sys, Ice                                                                                 # Import the sys and Ice libraries (Ice runtime).
import NumberGuessingGame                                                                       # Import the NumberGuessingGame module (proxies and skeletons).
import argparse                                                                                 # Import the argparse library for cmd arguments.
import random                                                                                   # Import the random library for random number generation.


class GameI(NumberGuessingGame.Game):
    """
    Class that implements the 'Game' interface.
    This class inherits from the 'Game' class in the 'NumberGuessingGame' module.

    Methods:
        checkGuess: Method that compares the received number with the correct one.
    """
    def __init__(self):
        self.target_number = random.randint(1, 100)
        # print(self.target_number)

    def checkGuess(self, guess, current=None):
        """Method that compares the received number with the correct one."""
        if guess > self.target_number:                                                          # Check if the guess is higher than the target number.
            return 'Your guess is HIGHER than the target number!'
        elif guess < self.target_number:                                                        # Check if the guess is lower than the target number.   
            return 'Your guess is LOWER than the target number!'
        else:                                                                                   # The guess is correct.
            print(f'You won! The correct number was {self.target_number} indeed.')
            return 'Correct'


def main() -> bool:
    """
    Main function.
    
    Returns:
        A boolean indicating the success of the process.
    """
    port = 10000                                                                                # Set the default port number.
    print(f'Listening port: {port}')                                                            # Print the port number.

    with Ice.initialize(sys.argv) as communicator:                                              # Initialize the Ice run time and create a communicator.

        adapter = communicator.createObjectAdapterWithEndpoints(                                # Create an object adapter with the name 'NumberGuessingGame' and an
            'NumberGuessingGameAdapter', f'default -p {port}'                                   # endpoint with the default protocol and the specified port number.
        )

        servant = GameI()                                                                       # Create an instance of the 'GameI' class.

        proxy = adapter.add(servant, communicator.stringToIdentity('NumberGuessingGame'))       # Add the 'servant' instance to the adapter with the identity 'NumberGuessingGame'.

        adapter.activate()                                                                      # Activate the adapter to make the servant available for incoming requests.
        communicator.waitForShutdown()                                                          # Wait for the communicator to be destroyed.

    return 0


if __name__ == '__main__':
    sys.exit(main())                                                                            # Call the main function and exit with the returned status code.
