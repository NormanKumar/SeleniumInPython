class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
        else:
            self.balance += amount
            print(amount,"is deposited to your Account", self.account_number)

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            print("Withdrawed", amount,"\nRemaining balance:", self.balance)

    def __del__(self):
        print("Account:",self.account_number,"has been  deleted.")

account1 = BankAccount(123456, 1000)

account1.deposit(500)
account1.withdraw(300)
account1.withdraw(2000)

del account1
