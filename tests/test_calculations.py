import pytest

from app.calculations import add, BankAccount, InsufficentFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(2, 3, 5), (4, 6, 10), (1, 1, 2)])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


def test_bank_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(24)
    assert bank_account.balance == 26


def test_deposit(bank_account):
    bank_account.deposit(24)
    assert bank_account.balance == 74


def test_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55.0


@pytest.mark.parametrize(
    "deposited, withdrew, expected",
    [(200, 100, 100), (50, 10, 40), (1200, 200, 1000)],
)
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficentFunds):
        bank_account.withdraw(200)
