from typing import Union

from fastapi import FastAPI
from fastapi import APIRouter

from pydantic import BaseModel

from app.functions import registration

app = FastAPI()
reg = registration()

router = APIRouter()

class Customerdetails(BaseModel):
    first_name: str
    last_name:str
    email_id:str
    phone:str
    province:str
    city:str
    postalcode:str

class CustomerEmail(BaseModel):
    email_id:str

@app.get("/")
def read_root():
    return {"Hello": "test app"}

@app.post("/customer-registration")
async def customer_registration(customerdetails: Customerdetails):
    cust_dict=customerdetails.dict()
    message=reg.insert_customer(cust_dict)
    print(message)
    return message

@app.post("/verify-registratration")
async def verify_registration(email: CustomerEmail):
    email_id = email.email_id
    message=reg.verify_registration(email_id)
    print(message)
    return message
