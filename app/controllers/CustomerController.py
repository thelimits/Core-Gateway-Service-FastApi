from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services.CustomerServices import CustomerServices
from dto.CustomerRequestDTO import CustomerRequestDTO
from dto.CustomerResponseDTO import CustomerResponseDTO
from dto.CustomerResponseDTO import CustomerPageResponseDTO
from dto.CustomerResponseDTO import CustomerPhoneNumberResponseDTO
from dto.CustomerResponseDTO import AuthResponseDTO
from dto.CustomerRequestDTO import AuthenticateCustomerDTO
from config.database import get_db
import model.CustomerKYC as model
from typing import List, Optional

router = APIRouter(
    prefix="/customers",
    tags=['Customers']
)

customer_service = CustomerServices()

get_Db = get_db


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=CustomerResponseDTO)
async def createCustomer(customer_request: CustomerRequestDTO,
                         db: Session = Depends(get_Db)):
    customer_data = customer_service.create_customer(customer_request, db)
    return customer_data

@router.post("/{id}",
              status_code=status.HTTP_200_OK,
              response_model=CustomerResponseDTO)
async def updateCustomer(id: str,
                         status: str,
                         db: Session = Depends(get_Db)):
    customer_update = await customer_service.update_customer(id, status, db)
    return customer_update

@router.patch("/details/{id}",
              status_code=status.HTTP_200_OK,
              response_model=CustomerResponseDTO)
async def updateCustomerDetails(id: str,
                                customer_request: CustomerRequestDTO,
                                db: Session = Depends(get_Db)):
    customer_update_details = customer_service.update_customer_detail(id, customer_request, db)
    return customer_update_details

@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=CustomerPageResponseDTO)
async def getCustomer(page: Optional[int] = 1,
                      size: Optional[int] = 15,
                      status: str = "",
                      order_by: Optional[str] = "desc,createdAt",
                      db: Session = Depends(get_Db)):
    data = {
        "page": page,
        "size": size,
        "status": status,
        "order_by": order_by,
    }
    customerDataAll = customer_service.get_customer(data, db)
    return customerDataAll


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=CustomerResponseDTO)
async def getCustomerById(id: str,
                          db: Session = Depends(get_Db)):
    customer = customer_service.get_customer_by_id(id, db)
    return customer

@router.get("/phone/{phoneNumber}",
            status_code=status.HTTP_200_OK,
            response_model=CustomerResponseDTO)
async def getByPhoneNumber(phoneNumber: str,
                          db: Session = Depends(get_Db)):
    customer = customer_service.get_customer_by_phone(phoneNumber, db)
    return customer

@router.get("/phone/{phoneNumber}/status",
            status_code=status.HTTP_200_OK,
            response_model=CustomerPhoneNumberResponseDTO)
async def getStatusByPhoneNumber(phoneNumber: str,
                          db: Session = Depends(get_Db)):
    customer = customer_service.get_customer_by_phone_status(phoneNumber, db)
    return customer

@router.post("/auth",
             status_code=status.HTTP_201_CREATED,
             response_model=AuthResponseDTO)
async def authentication(customer_request: AuthenticateCustomerDTO,
                         db: Session = Depends(get_Db)):
    customer_data = customer_service.authentication(customer_request, db)
    return customer_data

@router.get("/search/name",
            status_code=status.HTTP_200_OK,
            response_model=CustomerPageResponseDTO)
async def searchCustomerByName(page: Optional[int] = 1,
                      size: Optional[int] = 15,
                      status: Optional [str] = None,
                      q: str = "",
                      order_by: Optional[str] = "desc,createdAt",
                      db: Session = Depends(get_Db)):
    data = {
        "page": page,
        "size": size,
        "status": status,
        "q": q,
        "order_by": order_by,
    }
    customerDataAll = customer_service.search_customer_by_name(data, db)
    return customerDataAll

@router.get("/search/nik",
            status_code=status.HTTP_200_OK,
            response_model=CustomerPageResponseDTO)
async def searchCustomerByNik(page: Optional[int] = 1,
                      size: Optional[int] = 15,
                      status: Optional [str] = None,
                      q: str = "",
                      order_by: Optional[str] = "desc,createdAt",
                      db: Session = Depends(get_Db)):
    data = {
        "page": page,
        "size": size,
        "status": status,
        "q": q,
        "order_by": order_by,
    }
    customerDataAll = customer_service.search_nik(data, db)
    return customerDataAll

@router.get("/search/phone",
            status_code=status.HTTP_200_OK,
            response_model=CustomerPageResponseDTO)
async def searchCustomerByNik(page: Optional[int] = 1,
                      size: Optional[int] = 15,
                      status: Optional [str] = None,
                      q: str = "",
                      order_by: Optional[str] = "desc,createdAt",
                      db: Session = Depends(get_Db)):
    data = {
        "page": page,
        "size": size,
        "status": status,
        "q": q,
        "order_by": order_by,
    }
    customerDataAll = customer_service.search_phone(data, db)
    return customerDataAll