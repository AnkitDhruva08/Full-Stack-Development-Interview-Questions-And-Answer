"""
An abstract method is a method that is declared but not defined;
it specifies a signature and requires subclasses to provide the concrete implementation.
These methods are part of an abstract class, which serves as a blueprint for other classes to follow.
Abstract methods cannot be instantiated and must be implemented by any non-abstract subclass that inherits from the abstract class
"""


from abc import ABC, abstractmethod

class Payment(ABC):

    @abstractmethod
    def pay(self, amount):
        """Every payment method must implement this method"""
        pass



class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Processing credit card payment of {amount}")


class PayPalPayment(Payment):
    def pay(self, amount):
        print(f"Processing PayPal payment of {amount}")
 

class UpiPayment(Payment):
    def pay(self, amount):
        print(f"Processing UPI payment of {amount}")



# main program

payments = [
    CreditCardPayment(),
    PayPalPayment(),
    UpiPayment(),
]


for payment in payments:
    payment.pay(100)
