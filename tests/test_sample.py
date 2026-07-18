from app.calculations import add,subtract,multiply,divide,BankAccount,Insufficient_balance
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def regular_bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected",[(4,5,9),(3,6,9),(23,43,66)])
def test_add(num1,num2,expected):
    assert add(4,5)==9

def test_sub():
    assert subtract(10,5)==5

def test_multiply():
    assert multiply(10,3)==30

def test_divide():
    assert divide(72,9)==8

def test_init():
    A=BankAccount(50)
    assert A.balance==50
def test_init_0(zero_bank_account):
    assert zero_bank_account.balance==0
def test_deposit():
    A=BankAccount(50)
    A.deposit(10)
    assert A.balance==60

def test_withdraw(regular_bank_account):
    regular_bank_account.withdraw(20)
    assert regular_bank_account.balance==30
def test_interest():
    A=BankAccount(50)
    A.collect_interest()
    assert round(A.balance,3)==55

@pytest.mark.parametrize("deposit,withdrew,expected",[(200,100,100),(50,10,40),(1600,750,850)])
def test_bank_transaction(zero_bank_account,deposit,withdrew,expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance==expected
    
def test_insufficient(regular_bank_account):
    with pytest.raises(Insufficient_balance):
        regular_bank_account.withdraw(200)