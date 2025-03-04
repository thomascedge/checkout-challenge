import httpx
from fastapi import FastAPI, HTTPException
from payment_gateway_api.utils import PaymentGateway, IDGenerator
from .model import Transaction, Status

app = FastAPI()
payment_gateway = PaymentGateway()
database = {}

"""
POST endpoints
"""
@app.post('/merchant')
async def create_new_merchant():
    """
    Creates a new merchant, giving them an individual merchant id.
    """
    merchant_id = IDGenerator().generate_merchant_id()
    database[merchant_id] = {}
    return {"merchant_id": merchant_id}

@app.post('/merchant/{merchant_id}/transaction')
async def payment_to_simulator(merchant_id: str, transaction: Transaction) -> dict:
    """
    Takes a transaction for an individual merchant, verifies it using the
    payment gateway, sends data to the bank simulator if necessary, and sends
    result to server.
    """
    transaction_details = payment_gateway.validate_transaction(transaction)
    id = transaction_details.id
    status = transaction_details.status
    message = ''

    if status == Status.REJECTED:
        database[merchant_id][id] = transaction_details
        message = 'Transaction rejected.'
        return {"id": id, "status_code": status, "message": message}
    
    # send transaction data to simulator hosted on port 8080 and get response
    try:
        url = 'http://localhost:8080/payments'
        response = await to_simulator(url, transaction.model_dump())
        data = response.json()
        authorized_flag = data['authorized']
    except HTTPException:
        print('Cannot connect to simulator.')

    if not authorized_flag:
        status = Status.DECLINED
        message = 'Transaction declined.'
    else:
        status = Status.AUTHROIZED
        message = 'Transaction authorized.'
    
    transaction_details = transaction_details.model_copy(update={"status": status})
    database[merchant_id][id] = transaction_details

    return {"id": id, "status_code": status, "message": message}

"""
GET endpoints
"""
@app.get('/merchant/{merchant_id}/transaction')
async def get_payments(merchant_id: str,) -> dict:
    """
    Get request that returns all transaction data for a given id.
    """
    if merchant_id not in database.keys():
        raise HTTPException(status_code=404, detail=f'No transaction history found.')
    return {"transaction_data": database[merchant_id]}

"""
Helper functions
"""
async def to_simulator(url, data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        return response
