from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

from app.functions import registration

app = FastAPI()
reg = registration()

class Customerdetails(BaseModel):
    first_name: str
    last_name:str
    email_id:str
    phone:str
    province:str
    city:str
    postacode:str

class CustomerEmail(BaseModel):
    email_id:str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/customer-registration")
async def customer_registration(customerdetails: Customerdetails):
    message=reg.insert_customer(customerdetails)
    print(message)
    return {message}

@app.post("/verify-registratration")
async def verify_registration(email: CustomerEmail):
    message=reg.verify_registration(email)
    print(message)
    return(message)
