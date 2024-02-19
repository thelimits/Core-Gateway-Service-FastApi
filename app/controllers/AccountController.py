from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.database import get_db
from typing import List, Optional
from services.AccountServices import AccountServices
from dto.AccountResponseDTO import AccountResponseDTO, AccountNoteResponseDTO, AccountNoteDTO
from dto.AccountRequestDTO import CreateAccountRequestDTO
from dto.AccountRequestDTO import CreateNoteRequestDTO
from dto.AccountRequestDTO import UpdateNoteRequestDTO
from dto.CustomerResponseDTO import CustomerResponseWithAccountDTO
router = APIRouter(
    prefix="/account",
    tags=['Account']
)

account_service = AccountServices()

get_Db = get_db

@router.post(
    "/create/saving-account/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountResponseDTO
)
async def createSavingAccount(
    id: str,
    request_body: CreateAccountRequestDTO,
    db: Session = Depends(get_Db)
):
    account_response = await account_service.create_saving_account(id, request_body, db)
    
    return account_response

@router.get("/customers/{id}",
            status_code=status.HTTP_200_OK,
            response_model=CustomerResponseWithAccountDTO)
async def getAccountCustomersById(
                    id: str,
                    db: Session = Depends(get_Db)):
    accountDataAll = account_service.get_account_by_customer_id(id, db)
    return accountDataAll

@router.get("/customers/account-number/{number}",
            status_code=status.HTTP_200_OK,
            response_model=CustomerResponseWithAccountDTO)
async def getAccountCustomersByAccountNumber(
                    number: str,
                    db: Session = Depends(get_Db)):
    accountDataAll = account_service.get_account_by_account_number(number, db)
    return accountDataAll

@router.get("/customers/search/name",
            status_code=status.HTTP_200_OK)
async def searchCustomerNameAndAccountType(
    q: str="",
    page: Optional[int] = 1,
    size: Optional[int] = 15,
    status: str = "",
    order_by: Optional[str] = "desc,createdAt",
    db: Session = Depends(get_Db)):
    data = {
        "q": q,
        "page": page,
        "size": size,
        "status": status,
        "order_by": order_by,
    }
    accountDataAll = account_service.search_customer_name_and_account_type(data, db)
    return accountDataAll

@router.post(
    "/create/note/{accountNumber}",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountNoteDTO
)
async def createAccountNote(
    accountNumber: str,
    request_body: CreateNoteRequestDTO,
    db: Session = Depends(get_Db)
):
    account_response = account_service.create_note(accountNumber, request_body, db)
    
    return account_response

@router.get("/note",
            status_code=status.HTTP_200_OK,
            response_model=AccountNoteResponseDTO)
async def getNote(
    account_number: str,
    db: Session = Depends(get_Db)):

    accountDataAll = account_service.get_note(account_number, db)
    return accountDataAll

@router.patch("/note",
              status_code=status.HTTP_200_OK)
async def updateNote(
    id: str,
    account_request: UpdateNoteRequestDTO,
    db: Session = Depends(get_Db)):
    accountDataAll = account_service.update_note(id, account_request, db)
    return accountDataAll

@router.delete("/note",
              status_code=status.HTTP_200_OK)
async def deleteNote(
    id: str,
    db: Session = Depends(get_Db)):
    accountDataAll = account_service.delete_note(id, db)
    return accountDataAll