from pydantic import BaseModel
from datetime import date

class CustomerRequestDTO(BaseModel):
    firstName: str
    lastName: str
    address: str
    nik: str
    dob: date
    motherMaidenName: str
    email: str
    pin: str
    phoneNumber: str

class AuthenticateCustomerDTO(BaseModel):
    phoneNumber: str
    pin: str