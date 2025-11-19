# this program is for ooops concepts that will cover topic of oops
# class, object, inheritance, polymorphism, encapsulation, abstraction, methods

# OOPs Concepts Explained Through a Banking System

# A Banking System is an ideal real-world example to demonstrate every major OOP concept in an organized and practical way. Let’s go through each concept in context.

# 1. Class and Object

# A class is a blueprint or template that defines the properties (data) and behaviors (methods) of an object.

# An object is a real-world entity or an instance of a class.

# Example in context:

# BankAccount can be a class that defines attributes like:

# accountNumber

# accountHolderName

# balance

# Each customer’s account (e.g., Ankit’s Account, Riya’s Account) will be an object of this class, having unique values for these properties.

# 2. Attributes and Methods

# Attributes (Data Members): Store the state or information of an object (like balance, name, account number).

# Methods (Member Functions): Define the actions or operations that can be performed (like deposit, withdraw, checkBalance).

# In banking terms:

# deposit(amount) → increases balance.

# withdraw(amount) → decreases balance (with validation).

# displayDetails() → shows customer details.

# These methods represent behaviors of the account.

# 3. Encapsulation

# Encapsulation is the concept of binding data and methods together into a single unit and restricting direct access to the internal data.

# It protects sensitive data from unauthorized access or modification.

# In banking terms:

# A customer’s balance should not be directly accessible or modified by external users.

# Instead of changing balance directly, users must call secure methods like deposit() or withdraw().

# Benefits:

# Data security (customers can’t modify balance directly)

# Controlled access (via getters/setters)

# Better maintainability

# 4. Abstraction

# Abstraction hides unnecessary implementation details from the user and only shows the essential features.

# In a banking system, customers only see what they need to use — not how it works internally.

# In banking terms:

# A customer uses an ATM interface to deposit or withdraw cash.

# They don’t know how the backend system verifies account details, updates databases, or communicates with other services.

# Abstract classes or interfaces (e.g., AccountService) define what actions can be done (like deposit, withdraw) but not how they’re performed.

# Benefit:
# Simplifies complex systems by showing only necessary features.

# 5. Inheritance

# Inheritance allows a class (child/subclass) to inherit properties and methods from another class (parent/superclass).

# It promotes code reusability and establishes a hierarchy.

# In banking terms:

# BankAccount can be the base class.

# Subclasses like:

# SavingsAccount

# CurrentAccount

# FixedDepositAccount
# can inherit common features (like account number, holder name, balance) and add their own:

# SavingsAccount may have an interest rate.

# CurrentAccount may allow overdrafts.

# FixedDepositAccount may have a maturity date.

# Benefit:
# Reduces redundancy and organizes account types logically.

# 6. Polymorphism

# Polymorphism means “many forms” — the ability to perform the same operation in different ways depending on the object type.

# There are two types:

# Compile-time (Method Overloading)

# Multiple methods with the same name but different parameters.

# e.g., calculateInterest() could work differently for monthly or yearly interest depending on input.

# Runtime (Method Overriding)

# A subclass provides a specific implementation of a method already defined in its parent class.

# e.g., withdraw() method:

# In SavingsAccount, may disallow withdrawal if balance < minimum.

# In CurrentAccount, may allow overdraft.

# Benefit:
# Gives flexibility and makes systems more dynamic.

# 7. Constructors and Destructors

# Constructor: A special method that initializes an object when it’s created.

# For example, when creating a new BankAccount, the constructor sets the account number, holder name, and initial balance.

# Destructor: A method that is called automatically when an object is destroyed or goes out of scope — used for cleanup operations (like closing connections or saving logs).

# In banking context:

# Constructor → initializes new account details.

# Destructor → logs account closure or updates database when an object is deleted.

# 8. Access Modifiers

# Access modifiers control visibility of class members.

# Types:

# Public: Accessible from anywhere (e.g., deposit() method).

# Private: Accessible only within the class (e.g., balance variable).

# Protected: Accessible within the class and its subclasses.

# In banking context:

# balance can be private, so external users cannot change it.

# calculateInterest() can be protected, as it’s needed only by subclasses.

# deposit() and withdraw() can be public, to allow customer actions.

# 9. Association, Aggregation, and Composition

# Association: General relationship between two classes (e.g., Bank ↔ Customer)

# Aggregation: "Has-A" relationship where one object can exist independently (e.g., Bank has multiple Accounts).

# Composition: Strong "Has-A" relationship where one object’s life depends on another (e.g., Account has TransactionHistory — if Account is deleted, its transactions are deleted too).

# Example:

# Bank class contains a list of Accounts (Aggregation)

# Each Account contains TransactionHistory (Composition)

# Customer is associated with Bank through accounts (Association)

# 10. Real-World Flow of OOPs in Banking System

# BankAccount class defines basic structure (Encapsulation).

# Derived classes like SavingsAccount and CurrentAccount extend it (Inheritance).

# Each derived class customizes common methods like withdraw() (Polymorphism).

# Only secure interfaces (ATM or app) are exposed to users (Abstraction).

# Access modifiers ensure data safety (Private, Protected, Public).

# ✅ Summary Table
# OOP Concept	Banking Example	Purpose
# Class & Object	BankAccount and actual customer account	Blueprint & instance
# Encapsulation	Private balance, secure deposit/withdraw methods	Data protection
# Abstraction	ATM hides backend complexity	Simplify interaction
# Inheritance	SavingsAccount inherits from BankAccount	Code reuse
# Polymorphism	Different withdraw() rules for accounts	Flexibility
# Constructor/Destructor	Setup and cleanup of account objects	Lifecycle management
# Access Modifiers	Public, private, protected	Control visibility
# Association/Aggregation/Composition



# Bank has Accounts; Account has TransactionHistory	Define relationships
# By implementing these OOP concepts, a banking system can be designed to be secure, maintainable, and scalable, closely mirroring real-world banking operations.
# Given an array arr[] with non-negative integers representing the height of blocks. If the width of each block is 1,

class BankAccount:
    