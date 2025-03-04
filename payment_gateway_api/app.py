import httpx
from fastapi import FastAPI, HTTPException
from payment_gateway_api.utils import PaymentGateway
from .model import Transaction, Status

app = FastAPI()
payment_gateway = PaymentGateway()
database = {}

"""
POST endpoints
"""
@app.post('/payments')
async def payment_to_simulator(transaction: Transaction) -> dict:
    transaction_details = payment_gateway.validate_transaction(transaction)
    id = transaction_details.id
    status = transaction_details.status
    message = ''

    if status == Status.REJECTED:
        database[id] = transaction_details
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
    database[id] = transaction_details

    return {"id": id, "status_code": status, "message": message}

"""
GET endpoints
"""
@app.get('/payments/{payment_id}')
async def get_payments(payment_id: str) -> dict:
    if id not in database.keys():
        raise HTTPException(status_code=404, detail=f'No transaction history for id, {payment_id}.')
    return {"transaction_data": database[payment_id]}
    

"""
Helper functions
"""
async def to_simulator(url, data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        return response
