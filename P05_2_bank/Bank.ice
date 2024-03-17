module Bank
{
    interface Account
    {
        double getBalance();
        void deposit(double amount);
        void withdraw(double amount);
        void shutdown();
    };
};