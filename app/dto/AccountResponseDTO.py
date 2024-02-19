from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional, Any, List
import pytz

class AdditionalDetailsDTO(BaseModel):
    sourceOfFunds: Optional[str]
    workPlace: Optional[str]
    rangeSalaries: Optional[str]
    purpose: Optional[str]
    
class AccountNoteDTO(BaseModel):
    note: str
    
class AccountResponseDTO(BaseModel):
    id: str
    accountName: str
    accountNumber: str
    stakeholderIds: str
    status: str
    type: str
    openingTimestamp: Optional[datetime]
    closingTimestamp: Optional[datetime]
    additionalDetails: Optional[AdditionalDetailsDTO] = None
    accountNote: Optional[List[AccountNoteDTO]] = None
    
    @validator("openingTimestamp", "closingTimestamp", pre=True, always=True)
    def convert_to_jakarta_timezone(cls, value):
        if value:
            try:
                jakarta_timezone = pytz.timezone('Asia/Jakarta')
                return value.replace(tzinfo=pytz.utc).astimezone(jakarta_timezone)
            except Exception as e:
                print(f"Error while converting datetime: {e}")
        return value
    
    class config:
        orm_mode = True
        
class AccountPageResponseDTO(BaseModel):
    """ The response for a pagination query. """
    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[AccountResponseDTO]
    
class AuthResponseDTO(BaseModel):
    authenticate: bool
    
    class config:
        orm_mode = True
        
class AccountNoteResponseDTO(BaseModel):
    accountNote: Optional[List[AccountNoteDTO]] = None
        
    class config:
        orm_mode= True