# Project Outline

Merchant should process payment through payment_gateway with one of three responses (below) and retrieve details of all payments
	
## Stored data
{} -> merchant : {} -> id: payment details

Card
    Card number
    Expiry month
    Expiry year
    CVV
Status
    Authorized: 0
    Declined: 1
    Rejected: 2

Money
    Currency
    Amount

Transaction
    Card
    Money

PaymentDetails
    ID -> GUID
    Status
    Card
    Money - Amount

	
## End points
*   POST
    * /payments -> str
        * Gets response from bank. If response is Rejected, do not send to gateway. Else send to gateway
        * Returns payment id and status
    * /payments/new-merchant -> str
        * Creates a merchant id for a new merchant
        * Takes no input
        * Returns merchant id
* GET
    * /payments/
    * /payments/merchant_id -> Dict[PaymentDetails]
        * Get all payments by merchant_id
        * Returns list of all payments
    * /payments/merchant_id/payment_id -> PaymentDetails
        * Get individual payment by merchant_id
        * Returns individual payment


## Testing