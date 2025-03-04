from pydantic import BaseModel
from enum import Enum

class Status(Enum):
    AUTHROIZED = 0
    DECLINED = 1
    REJECTED = 2

class Transaction(BaseModel):
    card_number: str
    cvv: str
    expiry_date: str
    amount: float
    currency: str

class TransactionDetails(BaseModel):
    id: str
    card_number: str
    cvv: str
    expiry_date: str
    amount: float
    currency: str
    status: Status
