from datetime import datetime
from uuid import uuid4
from .model import Status, Transaction, TransactionDetails

class IDGenerator():
    def __init__(self):
        pass

    def generate_merchant_id(self):
        """
        Creatus a uuid for a given merchant
        """
        return str(uuid4())[:5]

    def generate_transaction_id(self):
        """
        Creates a uuid for a given shopper
        """
        return str(uuid4())


class PaymentGateway():
    def __init__(self):
        pass

    def validate_transaction(self, transaction: Transaction) -> bool:
        """
        Validates transaction request
        """
        status = None
        id = IDGenerator().generate_transaction_id()
        last_four_digits = transaction.card_number[-4::]
        expiry_month = int(transaction.expiry_date[:2])
        expiry_year = int(transaction.expiry_date[3:])


        card_number_valid = self._validate_card_number(transaction.card_number) 
        expiry_month_valid = self._validate_expiry_month(expiry_month)
        expiry_year_valid = self._validate_expiry_year(expiry_year)
        currency_code_valid = self._validate_currency_code(transaction.currency)
        amount_valid = self._validate_amount(transaction.amount)
        cvv_valid = self._validate_cvv(transaction.cvv)

        valid_transaction = card_number_valid & \
                            expiry_month_valid & \
                            expiry_year_valid & \
                            currency_code_valid & \
                            amount_valid & \
                            cvv_valid

        # if transaction validation fails, send 'Rejected' 
        # as the status for the response
        status = Status.REJECTED if not valid_transaction else Status.AUTHROIZED
            
        transaction_details = TransactionDetails(
            id=id,
            card_number=transaction.card_number,
            cvv=transaction.cvv,
            expiry_date=transaction.expiry_date,
            amount=transaction.amount,
            currency=transaction.currency,
            status=status,
        )

        return transaction_details

    ### internal helper functions ###

    def _validate_card_number(self, card_number: str) -> bool:
        """
        Returns true if card number is between 14-19 characters long and only 
        contains only numeric characters.
        """
        # validate request based on card_number and currency
        # if information not valid then reject
        if len(card_number) not in range(14, 20) or not card_number.isdigit():
            return False
        return True

    def _validate_expiry_month(self, expiry_month: str) -> bool:
        """
        Returns true if expiry month is be between 1-12
        """
        if 1 < expiry_month < 12:
            return True
        return False
    
    def _validate_expiry_year(self, expiry_year: str) -> bool:
        """
        Returns true if expiry year is in the future.	
        NOTE: Ensure the combination of expiry month + year is in the future
        """
        today = datetime.today()

        if expiry_year < today.year:
            return False
        return True
    
    def _validate_currency_code(self, currency_code: str) -> bool:
        """
        Returns true if currency code is 3 characters and represents countries
        United States (USD), Canada (CAD), and Mexico (MXN)
        """
        if len(currency_code) != 3 or currency_code not in ['USD', 'CAD', 'GBP']:
            return False
        return True
    
    def _validate_amount(self, amount: float):
        """
        Returns true if amount is an integer
        """
        return isinstance(amount, float)

    def _validate_cvv(self, cvv: str):
        """
        Returns true if CVV is 3-4 characters long and only contains numeric 
        characters
        """
        if len(cvv) not in [3, 4] or not cvv.isdigit():
            return False
        return True
