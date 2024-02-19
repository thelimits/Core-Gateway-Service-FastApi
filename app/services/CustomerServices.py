import model.CustomerKYC as modelCustomer
from fastapi import HTTPException, status
from model.enum.CustomerStatusType import CustomerStatusType
from dto.CustomerRequestDTO import CustomerRequestDTO
from dto.CustomerRequestDTO import AuthenticateCustomerDTO
from repository.CustomerRepository import CustomerRepository
from sqlalchemy.orm import Session
from sqlalchemy import func
from services.ThoughtMachineApiClient import ThoughtMachineApiClient
from services.ThoughtMachineApiClient import Configuration
from model.enum.Endpoint import Endpoint

import uuid

# repository
repository = CustomerRepository()

# TM Api Client
configuration = Configuration()
client = ThoughtMachineApiClient(configuration)

class CustomerServices:
    def __init__(self):
        pass
            
    def create_customer(self, customer_request : CustomerRequestDTO, 
                        db: Session):
        random_uuid = uuid.uuid4()
        
        create_cust = modelCustomer.CustomerKYC(
                id = str(random_uuid), 
                **vars(customer_request), 
                status=CustomerStatusType.PENDING.value
            )
        db.add(create_cust)
        db.commit()
        db.refresh(create_cust)

        return create_cust
    
    async def update_customer(self, id: str, status_cust: str,
                        db: Session):
        
        user = repository.get_customer_by_id(
            id=id,
            db=db
        )
        
        valid_status_values = [e.value for e in CustomerStatusType]
        if status_cust.upper() not in valid_status_values:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid status customer")
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id: {id} does not exist")
        activated= None
        if status_cust.upper() == CustomerStatusType.ACTIVE.value:
            requestId= str(uuid.uuid4())
            body = {
                "request_id": requestId,
                "customer": {
                    "id": user.first().id,
                    "status": f"CUSTOMER_STATUS_{CustomerStatusType.ACTIVE.value}",
                    "customer_details": {
                        "first_name": user.first().firstName,
                        "last_name": user.first().lastName
                    }
                }
            }
            
            try:
                await client.post(body=body, urls=Endpoint.CUSTOMERS.value)
                
            except HTTPException as e:
                print(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error Posting")
                
            activated = func.now()
            
        user.update({"status" : status_cust.upper(), 
                     'activatedAt': activated}, synchronize_session=False)
        db.commit()
            
        return user.first()
    
    def update_customer_detail(self, id: str, customer_request : CustomerRequestDTO, 
                        db: Session):
        user = repository.get_customer_by_id(
            id=id,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id: {id} does not exist")
            
        update_data = {**vars(customer_request)}
        
        user.update(update_data, synchronize_session=False)
        db.commit()
        
        return user.first()
    
    def get_customer(self, data : dict(),  
                     db: Session):
        split_order = data['order_by'].split(",")
        sort_order, sort_by = split_order[0], split_order[1]
        
        column_mapping = {
                "createdAt": modelCustomer.CustomerKYC.createdAt, 
                "activatedAt": modelCustomer.CustomerKYC.activatedAt
            }
        
        # periksa apakah sort_by valid
        if sort_by not in column_mapping:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid sorting column")
        
        # periksa apakah sort_order valid
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid sorting order")
        
        # periksa status apakah valid
        valid_status_values = [e.value for e in CustomerStatusType]
        if data['status'].upper() not in valid_status_values:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid status customer")
    
        all_customer = repository.get_all_customers(
            sort_by=sort_by,
            sort_order=sort_order,
            column_mapping=column_mapping,
            filter=data,
            db=db
        )
        
        return all_customer
    
    def get_customer_by_id(self, id: str, db: Session):
        
        user = repository.get_customer_by_id(
            id=id,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id: {id} does not exist")
            
        return user.first()
    
    def get_customer_by_phone(self, phoneNumber: str, db: Session):
    
        user = repository.get_customer_by_phone_number(
            phoneNumber=phoneNumber,
            db=db
        )
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with phoneNumber: {phoneNumber} does not exist")
            
        return user

    def get_customer_by_phone_status(self, phoneNumber: str, db: Session):
    
        user = repository.get_customer_by_phone_number(
            phoneNumber=phoneNumber,
            db=db
        )
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with phoneNumber: {phoneNumber} does not exist")
            
        return user
    
    def authentication(self, customer_request : AuthenticateCustomerDTO, 
                        db: Session):
        
        user = repository.get_customer_by_phone_number(
            phoneNumber=customer_request.phoneNumber,
            db=db
        )

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with phoneNumber: {customer_request.phoneNumber} does not exist")

        response = {
            "authenticate": True
        }
        
        return response
    
    def search_customer_by_name(self, data : dict(),  
                        db: Session):
        
        split_order = data['order_by'].split(",")
        sort_order, sort_by = split_order[0], split_order[1]
        
        column_mapping = {
                "createdAt": modelCustomer.CustomerKYC.createdAt, 
                "activatedAt": modelCustomer.CustomerKYC.activatedAt
            }
        
        # periksa apakah sort_by valid
        if sort_by not in column_mapping:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid sorting column")
        
        # periksa apakah sort_order valid
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid sorting order")
            
        # periksa status apakah valid
        valid_status_values = [e.value for e in CustomerStatusType]
        if data['status'] is not None and data['status'].upper() not in valid_status_values:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid status customer : [{valid_status_values}]")
        
        all_customer = repository.search_customer_by_name(
                sort_by=sort_by,
                sort_order=sort_order,
                column_mapping=column_mapping,
                filter=data,
                db=db
            )
            
        return all_customer

    def search_nik(self, data : dict(),  
                        db: Session):
            split_order = data['order_by'].split(",")
            sort_order, sort_by = split_order[0], split_order[1]
            
            column_mapping = {
                    "createdAt": modelCustomer.CustomerKYC.createdAt, 
                    "activatedAt": modelCustomer.CustomerKYC.activatedAt
                }
            
            # periksa apakah sort_by valid
            if sort_by not in column_mapping:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid sorting column")
            
            # periksa apakah sort_order valid
            if sort_order not in ["asc", "desc"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid sorting order")
            
            # periksa status apakah valid
            valid_status_values = [e.value for e in CustomerStatusType]
            if data['status'] is not None and data['status'].upper() not in valid_status_values:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Invalid status customer : [{valid_status_values}]")
        
            all_customer = repository.search_customer_by_nik(
                sort_by=sort_by,
                sort_order=sort_order,
                column_mapping=column_mapping,
                filter=data,
                db=db
            )
            
            return all_customer
    
    def search_phone(self, data : dict(),  
                    db: Session):
        split_order = data['order_by'].split(",")
        sort_order, sort_by = split_order[0], split_order[1]
        
        column_mapping = {
                "createdAt": modelCustomer.CustomerKYC.createdAt, 
                "activatedAt": modelCustomer.CustomerKYC.activatedAt
            }
        
        # periksa apakah sort_by valid
        if sort_by not in column_mapping:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid sorting column")
        
        # periksa apakah sort_order valid
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid sorting order")
            
        # periksa status apakah valid
        valid_status_values = [e.value for e in CustomerStatusType]
        if data['status'] is not None and data['status'].upper() not in valid_status_values:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid status customer : [{valid_status_values}]")
    
        all_customer = repository.search_customer_by_phone(
            sort_by=sort_by,
            sort_order=sort_order,
            column_mapping=column_mapping,
            filter=data,
            db=db
        )
        
        return all_customer