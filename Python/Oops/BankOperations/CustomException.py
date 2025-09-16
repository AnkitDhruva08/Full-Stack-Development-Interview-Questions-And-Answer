from abc import ABC, abstractmethod
import json

# ------------------- Custom Exception -------------------
class InsufficientFundsError(Exception):
    pass

# ------------------- Abstract Base Class -------------------
class Account(ABC):
    @abstractmethod
    def deposit(self, amount): pass

    @abstractmethod
    def withdraw(self, amount): pass


# ------------------- BankAccount (Base Class) -------------------
class BankAccount(Account):
    account_counter = 1000   # class variable

    def __init__(self, holder_name, balance=0.0):
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.holder_name = holder_name
        self.__balance = balance  # Encapsulation (private attribute)

    # Encapsulation → Getter
    def get_balance(self):
        return self.__balance

    # Deposit
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"✅ {amount} deposited. New Balance: {self.__balance}")
        else:
            print("❌ Invalid deposit amount.")

    # Withdraw
    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Invalid withdraw amount.")
            return
        if amount > self.__balance:
            raise InsufficientFundsError("❌ Not enough balance!")
        self.__balance -= amount
        print(f"✅ {amount} withdrawn. Remaining Balance: {self.__balance}")

    def check_balance(self):
        return self.__balance

    # Polymorphism → same method, diff behavior in child classes
    def calculate_interest(self):
        return 0

    @staticmethod
    def validate_account_number(acc_no):
        return isinstance(acc_no, int) and acc_no > 0


# ------------------- Derived Classes -------------------
class SavingsAccount(BankAccount):
    def __init__(self, holder_name, balance=0.0, interest_rate=0.05):
        super().__init__(holder_name, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        return self.get_balance() * self.interest_rate


class CurrentAccount(BankAccount):
    def __init__(self, holder_name, balance=0.0, overdraft_limit=1000):
        super().__init__(holder_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Invalid withdraw amount.")
            return
        if amount > self.get_balance() + self.overdraft_limit:
            raise InsufficientFundsError("❌ Overdraft limit exceeded!")
        # protected withdraw (access private balance through base withdraw)
        try:
            super().withdraw(amount)
        except InsufficientFundsError:
            # allow overdraft
            new_balance = self.get_balance() - amount
            print(f"✅ Overdraft used. Balance: {new_balance}")


# ------------------- Composition: Bank Class -------------------
class Bank:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        self.accounts[account.account_number] = account

    def get_account(self, acc_no):
        return self.accounts.get(acc_no, None)

    def transfer(self, from_acc, to_acc, amount, note=""):
        if from_acc.get_balance() < amount:
            raise InsufficientFundsError("❌ Transfer failed. Insufficient funds.")
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        print(f"✅ Transfer of {amount} successful. Note: {note}")

    # File Handling (Save to JSON)
    def save_to_file(self, filename="accounts.json"):
        data = {
            acc_no: {
                "holder_name": acc.holder_name,
                "balance": acc.get_balance(),
                "type": acc.__class__.__name__
            } for acc_no, acc in self.accounts.items()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("💾 Accounts saved to file.")

    # Load from JSON
    def load_from_file(self, filename="accounts.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            for acc_no, details in data.items():
                if details["type"] == "SavingsAccount":
                    acc = SavingsAccount(details["holder_name"], details["balance"])
                else:
                    acc = CurrentAccount(details["holder_name"], details["balance"])
                acc.account_number = int(acc_no)  # keep old acc_no
                self.accounts[int(acc_no)] = acc
            print("📂 Accounts loaded from file.")
        except FileNotFoundError:
            print("⚠️ No saved accounts found.")


# ------------------- Menu Driven System (Switch Case Style) -------------------
def main():
    bank = Bank()
    bank.load_from_file()

    while True:
        print("\n===== BANK MENU =====")
        print("1. Create Savings Account")
        print("2. Create Current Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Check Balance")
        print("7. Save & Exit")

        choice = input("Enter choice: ")

        # Switch-case using dictionary
        actions = {
            "1": lambda: create_account(bank, "savings"),
            "2": lambda: create_account(bank, "current"),
            "3": lambda: deposit_money(bank),
            "4": lambda: withdraw_money(bank),
            "5": lambda: transfer_money(bank),
            "6": lambda: check_balance(bank),
            "7": lambda: exit_program(bank)
        }

        action = actions.get(choice)
        if action:
            action()
        else:
            print("❌ Invalid choice.")


# ------------------- Helper Functions -------------------
def create_account(bank, acc_type):
    name = input("Enter holder name: ")
    amount = float(input("Enter initial deposit: "))
    if acc_type == "savings":
        acc = SavingsAccount(name, amount)
    else:
        acc = CurrentAccount(name, amount)
    bank.add_account(acc)
    print(f"✅ {acc_type.capitalize()} Account created. Account No: {acc.account_number}")

def deposit_money(bank):
    acc_no = int(input("Enter account number: "))
    acc = bank.get_account(acc_no)
    if acc:
        amount = float(input("Enter amount: "))
        acc.deposit(amount)
    else:
        print("❌ Account not found.")

def withdraw_money(bank):
    acc_no = int(input("Enter account number: "))
    acc = bank.get_account(acc_no)
    if acc:
        amount = float(input("Enter amount: "))
        try:
            acc.withdraw(amount)
        except InsufficientFundsError as e:
            print(e)
    else:
        print("❌ Account not found.")

def transfer_money(bank):
    from_acc_no = int(input("From Account No: "))
    to_acc_no = int(input("To Account No: "))
    amount = float(input("Enter amount: "))

    from_acc = bank.get_account(from_acc_no)
    to_acc = bank.get_account(to_acc_no)

    if from_acc and to_acc:
        try:
            bank.transfer(from_acc, to_acc, amount, note="Fund Transfer")
        except InsufficientFundsError as e:
            print(e)
    else:
        print("❌ One of the accounts not found.")

def check_balance(bank):
    acc_no = int(input("Enter account number: "))
    acc = bank.get_account(acc_no)
    if acc:
        print(f"💰 Balance for {acc.holder_name}: {acc.get_balance()}")
    else:
        print("❌ Account not found.")

def exit_program(bank):
    bank.save_to_file()
    print("👋 Exiting Bank System...")
    exit()


# ------------------- Run Program -------------------
if __name__ == "__main__":
    main()
