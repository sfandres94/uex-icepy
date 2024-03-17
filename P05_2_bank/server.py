#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Server script that simulates a bank operator.

Usage: python3 server.py

Author: Andres J. Sanchez-Fernandez
Email: sfandres@unex.es
Date: 2024-03-17
Version: v1
"""


# Import the 'sys' and 'Ice' libraries.
import sys, Ice

# Import the 'Bank' module.
import Bank


class AccountI(Bank.Account):
    """
    Class that inherits from the 'Account' class in the 'Bank' module.
    
    Attributes:
        balance (float): The current account balance.
    
    Methods:
        getBalance: Returns the account balance.
        deposit (amount): Increases the account balance.
        withdraw (amount): Decreases the account balance.
        shutdown (current): Shuts down the server.
    """
    def __init__(self):
        """Constructor of the class, which sets up the account."""
        self.balance = 0.0
        print('\nBank account successfully opened!')

    def getBalance(self, current=None):
        """Gets the account balance."""
        print('\nCurrent balance retrieved')
        return self.balance

    def deposit(self, amount, current=None):
        """Increases the account balance."""
        print('\nInitiating deposit...')
        self.balance += amount
        print('Deposit successfully completed!')

    def withdraw(self, amount, current=None):
        """Decreases the account balance."""
        print('\nInitiating withdrawal...')
        if amount > self.balance:
            raise ValueError('Insufficient funds')
        self.balance -= amount
        print('Withdrawal successfully completed!')

    def shutdown(self, current):
        """Shuts down the server."""
        print('\nShutting down...')
        current.adapter.getCommunicator().shutdown()


def main():
    """
    Main function.

    Returns:
        A boolean indicating the success of the process.
    """
    # Configure the listening port.
    port = 10000
    print(f'Listening port: {port}')

    # Initialize the Ice communicator.
    with Ice.initialize(sys.argv) as communicator:

        # Create a new object adapter with the name
        # 'SimpleBank' and the specified listening port.
        adapter = communicator.createObjectAdapterWithEndpoints(
            'SimpleBank', f'default -p {port}'
        )

        # Create a new instance of the 'AccountI' class.
        servant = AccountI()

        # Add the 'servant' to the 'adapter' with the identity 'Account'.
        adapter.add(servant, communicator.stringToIdentity('Account'))

        # Activate the adapter.
        adapter.activate()

        # Wait for the server to be shut down.
        communicator.waitForShutdown()

    return 0


# Call the main function and exit with the returned status code.
if __name__ == '__main__':
    sys.exit(main())
