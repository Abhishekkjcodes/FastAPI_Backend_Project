def add(num1,num2):
    print("sum calculation")
    return num1+num2

def subtract(num1,num2):

    return num1-num2

def multiply(num1,num2):

    return num1*num2

def divide(num1,num2):
    return num1/num2

class Insufficient_balance(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if(self.balance<amount):
            raise Insufficient_balance("Insufficient balance")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1