from datetime import datetime

import pytest

from .utils import Util
from .model import Request

util = Util()

request0 = Request(
    card_number='2222405343248877',
    expiry_date="04/2025",
    currency="USD",
    amount=int(100),
    cvv="123"
)

request1 = Request(
    card_number='222240A',
    expiry_date="14/2021",
    currency="RUB",
    amount=100,
    cvv="123A"
)

def test_validate_card_number():
    assert isinstance(util._validate_card_number(request0.card_number), bool)
    assert util._validate_card_number(request0.card_number) == True
    assert util._validate_card_number(request1.card_number) == False

def test_validate_expiry_month():
    assert isinstance(util._validate_expiry_month(request0.expiry_date), bool)
    assert util._validate_expiry_month(request0.expiry_date) == True
    assert util._validate_expiry_month(request1.expiry_date) == False

def test_validate_expiry_year():
    assert isinstance(util._validate_expiry_year(request0.expiry_date), bool)
    assert util._validate_expiry_year(request0.expiry_date) == True
    assert util._validate_expiry_year(request1.expiry_date) == False

def test_validate_currency_code():
    assert isinstance(util._validate_currency_code(request0.currency), bool)
    assert util._validate_currency_code(request0.currency) == True
    assert util._validate_currency_code(request1.currency) == False

def test_validate_amount():
    assert isinstance(util._validate_amount(request0.amount), bool)
    assert util._validate_amount(request0.amount) == True
    assert util._validate_amount(100.5) == False

def test_validate_cvv():
    assert isinstance(util._validate_cvv(request0.cvv), bool)
    assert util._validate_cvv(request0.cvv) == True
    assert util._validate_cvv(request1.cvv) == False