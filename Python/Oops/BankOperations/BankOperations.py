"""
Bank Operation – OOP Demonstration

Abstraction

Create an abstract base class BankAccount (cannot be instantiated directly).

It should define abstract methods like deposit(), withdraw(), and get_balance().

Concrete classes (like SavingsAccount, CurrentAccount) must implement these methods.

Encapsulation

Keep account details (like __balance, __account_number) private.

Provide public methods (deposit(), withdraw(), get_balance()) to safely access or modify balance.

Inheritance

SavingsAccount and CurrentAccount inherit from BankAccount.

They may have specific rules (e.g., minimum balance for savings, overdraft for current).

Polymorphism

Same method names (withdraw(), deposit()) behave differently depending on account type.

For example, SavingsAccount.withdraw() may restrict withdrawals if below minimum balance, while CurrentAccount.withdraw() may allow overdraft.
"""


from abc import ABC, abstractmethod

# 🔹 Abstraction: Abstract Base Class
class BankAccount(ABC):
    def __init__(self, bank, ac_no, balance):
        self.__ac_no = ac_no         
        self.__balance = balance      
        self.bank = bank

    # Encapsulation: Provide getter methods
    def get_account_no(self):
        return self.__ac_no
    
    def get_balance(self):
        return self.__balance
    
    # Encapsulation: Provide safe update methods
    def _set_balance(self, new_balance):
        self.__balance = new_balance

    # Abstract methods (must be implemented by subclasses)
    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass
    

    
# 🔹 Inheritance + Polymorphism
class SavingsAccount(BankAccount):
    def __init__(self, bank, ac_no, balance, min_balance=500):
        super().__init__(bank, ac_no, balance)
        self.min_balance = min_balance

    def deposit(self, amount):
        self._set_balance(self.get_balance() + amount)
        return f"Deposited {amount}, New Balance: {self.get_balance()}"

    def withdraw(self, amount):
        if self.get_balance() - amount < self.min_balance:
            return f"❌ Withdrawal denied! Minimum balance of {self.min_balance} must be maintained."
        else:
            self._set_balance(self.get_balance() - amount)
            return f"Withdrew {amount}, Remaining Balance: {self.get_balance()}"
        


class CurrentAccount(BankAccount):
    def __init__(self, bank, ac_no, balance, overdraft_limit=1000):
        super().__init__(bank, ac_no, balance)
        self.overdraft_limit = overdraft_limit

    def deposit(self, amount):
        self._set_balance(self.get_balance() + amount)
        return f"Deposited {amount}, New Balance: {self.get_balance()}"

    def withdraw(self, amount):
        if self.get_balance() - amount < -self.overdraft_limit:
            return f"❌ Withdrawal denied! Overdraft limit {self.overdraft_limit} exceeded."
        else:
            self._set_balance(self.get_balance() - amount)
            return f"Withdrew {amount}, Remaining Balance: {self.get_balance()}"


# 🔹 Main Program (Polymorphism in Action)
if __name__ == "__main__":
    s_acc = SavingsAccount("SBI", 101, 2000)
    c_acc = CurrentAccount("HDFC", 202, 500)

    # Polymorphism: Same method behaves differently
    print(s_acc.deposit(1000))  
    print(s_acc.withdraw(1800))  
    print(s_acc.withdraw(600))  

    print(c_acc.deposit(2000))   
    print(c_acc.withdraw(2500))  
    print(c_acc.withdraw(2000)) 




    
        