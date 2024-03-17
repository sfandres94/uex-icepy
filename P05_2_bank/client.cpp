/*
 * Author: A.J. Sanchez-Fernandez
 * Date: 17/03/2024
 * Description: Client script that simulates a bank operator.
 */


// Include the Ice library and Bank.h header files.
#include <Ice/Ice.h>
#include <Bank.h>
#include <stdexcept>

// Using the Bank namespace.
using namespace Bank;


// Main function.
int main(int argc, char* argv[])
{
    try
    {
        // Host and port values are set.
        std::string host = "localhost";
        int port = 10000;
        std::cout << "Host: " << host << " (connecting port: "
        << port << ")" << std::endl;

        // Initializing a communicator and creating a proxy.
        Ice::CommunicatorHolder ich(argc, argv);
        auto base = ich->stringToProxy(
            "Account:default -h "+ host + " -p " + std::to_string(port)
        );
        auto account = Ice::checkedCast<AccountPrx>(base);

        // Checking if the proxy is valid.
        if(!account)
        {
            throw std::runtime_error("Invalid proxy");
        }

        // User interaction loop.
        while (true)
        {
            int option;
            double amount;
            std::cout << std::endl;
            std::cout << "Enter operation (1: Get current balance, "
            "2: Deposit, 3: Withdraw, 4: Shutdown server and exit): ";
            std::cin >> option;

            switch (option)
            {
                case 1:
                    // Retrieving current balance and displaying it
                    // to the user.
                    std::cout << "Current balance: "
                    << account->getBalance() << std::endl;
                    break;

                case 2:
                    // Prompting the user to enter deposit amount,
                    // depositing it, and displaying success message.
                    std::cout << "Enter amount to deposit: ";
                    std::cin >> amount;
                    account->deposit(amount);
                    std::cout << "Deposit successful" << std::endl;
                    break;

                case 3:
                    // Prompting the user to enter withdrawal amount, 
                    // withdrawing it, and displaying success message.
                    std::cout << "Enter amount to withdraw: ";
                    std::cin >> amount;
                    account->withdraw(amount);
                    std::cout << "Withdrawal successful" << std::endl;
                    break;

                case 4:
                    // Sending a shutdown command to the server and
                    // exiting the program.
                    std::cout << "Shutting down the server and exiting"
                    << std::endl;    
                    account->shutdown();      
                    return 0;

                default:
                    // Displaying an error message for invalid
                    // user input.
                    std::cout << "Invalid option. Please try again."
                    << std::endl;
                    break;
            }
        }
    }
    catch(const std::exception& e)
    {
        // Displaying an error message for any exceptions.
        std::cerr << e.what() << std::endl;
        return 1;
    }

    return 0;
}
