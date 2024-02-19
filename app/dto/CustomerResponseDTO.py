from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional, Any, List
from dto.AccountResponseDTO import AccountResponseDTO
from model.CustomerAccount import CustomerAccount
import pytz

class CustomerResponseDTO(BaseModel):
    id: str
    firstName: str
    lastName: str
    address: str
    nik: str
    dob: date
    motherMaidenName: str
    email: str
    status: str
    phoneNumber: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    activatedAt: Optional[datetime]
    
    @validator("createdAt", "updatedAt", "activatedAt", pre=True, always=True)
    def convert_to_jakarta_timezone(cls, value):
        if value:
            try:
                jakarta_timezone = pytz.timezone('Asia/Jakarta')
                return value.replace(tzinfo=pytz.utc).astimezone(jakarta_timezone)
            except Exception as e:
                print(f"Error while converting datetime: {e}")
        return value
        
    class config:
        orm_mode= True
        
class CustomerResponseWithAccountDTO(BaseModel):
    id: str
    firstName: str
    lastName: str
    address: str
    nik: str
    dob: date
    motherMaidenName: str
    email: str
    status: str
    phoneNumber: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    activatedAt: Optional[datetime]
    accounts:  Optional[List[AccountResponseDTO]]

    @validator("createdAt", "updatedAt", "activatedAt", pre=True, always=True)
    def convert_to_jakarta_timezone(cls, value):
        if value:
            try:
                jakarta_timezone = pytz.timezone('Asia/Jakarta')
                return value.replace(tzinfo=pytz.utc).astimezone(jakarta_timezone)
            except Exception as e:
                print(f"Error while converting datetime: {e}")
        return value
    
    class config:
        orm_mode= True
        
        
class CustomerPageResponseDTO(BaseModel):
    """ The response for a pagination query. """
    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    customers: List[CustomerResponseDTO] | List[CustomerResponseWithAccountDTO]
    
    class config:
        orm_mode= True
    
class CustomerPhoneNumberResponseDTO(BaseModel):
    phoneNumber: str
    status: str
    
    class config:
        orm_mode= True

class AuthResponseDTO(BaseModel):
    authenticate: bool
    
    class config:
        orm_mode= True