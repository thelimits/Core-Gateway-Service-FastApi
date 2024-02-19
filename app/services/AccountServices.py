import model.CustomerAccount as modelAccount
import model.AccountNote as accountNote
import model.AccountAdditionalDetails as modelAccountDetails
from model.enum.CustomerStatusType import CustomerStatusType
from model.enum.AccountSatusType import AccountSatusType
from model.enum.AccountType import AccountType
from fastapi import HTTPException, status
from utils.GenerateAccountNumber import GenerateAccountNumber
from dto.AccountRequestDTO import CreateAccountRequestDTO
from sqlalchemy.orm import Session
from repository.CustomerRepository import CustomerRepository
from repository.AccountRepository import AccountRepository
from services.ThoughtMachineApiClient import ThoughtMachineApiClient
from services.ThoughtMachineApiClient import Configuration
from model.enum.Endpoint import Endpoint
from sqlalchemy import func
import uuid
import model.CustomerKYC as modelCustomer
from dto.AccountRequestDTO import CreateNoteRequestDTO
from dto.AccountRequestDTO import UpdateNoteRequestDTO

generate_account_number = GenerateAccountNumber()

# repository
customer_repository = CustomerRepository()
account_repository = AccountRepository()


# TM Api Client
configuration = Configuration()
client = ThoughtMachineApiClient(configuration)

class AccountServices:
    def __init__(self):
        pass
    
    async def create_saving_account(self, id: str, request_body: CreateAccountRequestDTO, db: Session):

        user = customer_repository.get_customer_by_id(
            id=id,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id: {id} does not exist")
            
        if user.first().status == CustomerStatusType.ACTIVE:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"User with id: {id} does not active customer")
            
        id_account_database = str(uuid.uuid4())
        
        create_account = None    
        if user.first().status == CustomerStatusType.ACTIVE.value:
            requestId= str(uuid.uuid4())
            accountId = f"CASA_{str(uuid.uuid4())}"
            
            # v2
            # body={
            #     "request_id": requestId,
            #     "account": {
            #         "id": accountId,
            #         "type": "ACCOUNT_TYPE_CUSTOMER",
            #         "product_version_id": request_body.productVersionId,
            #         "stakeholder_ids": [
            #             user.first().id
            #         ],
            #         "alias": request_body.accountName,
            #         "status": f"ACCOUNT_STATUS_{AccountSatusType.OPEN.value}",
            #         "permitted_denominations": [
            #             request_body.baseCurrency
            #         ]
            #     },
            #     "create_options": {
            #         "parameter_values": {
            #             "account_tier_names": {
            #                 "string_value": [
            #                     request_body.instanceParameter.accountTierNames.upper()
            #                 ]
            #             },
            #             "inactivity_fee_application_day": {
            #                 "string_value": request_body.instanceParameter.inactivityFeeApplicationDay
            #             },
            #             "interest_application_day": {
            #                 "string_value": request_body.instanceParameter.interestApplicationDay
            #             },
            #             "maintenance_fee_application_day": {
            #                 "string_value": request_body.instanceParameter.maintenanceFeeApplicationDay
            #             },
            #             "daily_withdrawal_limit_by_transaction_type": {
            #                 "string_value": request_body.instanceParameter.dailyWithdrawalLimitByTransactionType
            #             }
            #         }
            #     }
            # }
            
            # v1
            body={
                "request_id": requestId,
                "account": {
                    "id": accountId[:35],
                    "product_version_id": request_body.productVersionId,
                    "name": request_body.accountName,
                    "stakeholder_ids": [
                        user.first().id
                    ],
                    "status": f"ACCOUNT_STATUS_{AccountSatusType.OPEN.value}",
                    "permitted_denominations": [
                        "EUR",
                        "USD",
                        "SGD",
                        "IDR"
                    ],
                    "instance_param_vals": {
                        "account_tier_names":f'["{request_body.instanceParameter.accountTierNames.upper()}"]',
                        "inactivity_fee_application_day": request_body.instanceParameter.inactivityFeeApplicationDay,
                        "interest_application_day": request_body.instanceParameter.interestApplicationDay,
                        "maintenance_fee_application_day": request_body.instanceParameter.maintenanceFeeApplicationDay,
                        "daily_withdrawal_limit_by_transaction_type": '{"ATM":' + '"' + str(request_body.instanceParameter.dailyWithdrawalLimitByTransactionType) + '"' + '}'
                    }
                }
            }
            
            try:
                await client.post(body=body, urls=Endpoint.ACCOUNTS_V1.value)
            except HTTPException as e:
                print(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error Posting")
            
            # insert to database
            create_account = modelAccount.CustomerAccount(
                id = id_account_database,
                accountName = request_body.accountName, 
                accountNumber = generate_account_number.generate_id(),
                stakeholderIds = accountId,
                status = AccountSatusType.OPEN.value,
                type = AccountType.SAVING.value,
                openingTimestamp = func.now(),
                customerId = user.first().id
            )
            db.add(create_account)
            
            if request_body.accountAdditionalDetails is not None:
                create_additional_det = modelAccountDetails.AccountAdditionalDetails(
                    **vars(request_body.accountAdditionalDetails),
                    accountId = id_account_database,
                    id = str(uuid.uuid4())
                )
                db.add(create_additional_det)
                
            db.commit()    
            db.refresh(create_account)
            db.refresh(create_additional_det)
            
        return create_account
    
    def get_account_by_customer_id(self, id: str, db: Session):
        
        user = account_repository.find_account_by_id_customer(
            id=id,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id: {id} does not exist")
            
        return user.first()
    
    def get_account_by_account_number(self, number: str, db: Session):
        
        user = account_repository.find_customer_by_account_number(
            number=number,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with account number: {number} does not exist")
            
        return user.first()
    
    def search_customer_name_and_account_type(self, data: dict(), db: Session):

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
        
        # user = account_repository.find_by_account_number(
        #     number=number,
        #     db=db
        # )

        user = account_repository.search_customer_by_name_and_account_type(
            sort_by=sort_by,
            sort_order=sort_order,
            column_mapping=column_mapping,
            filter=data,
            db=db
        )
        
        return user
    
    def create_note(self, number: str, request_body: CreateNoteRequestDTO, db: Session):
        user = account_repository.find_by_account_number(
            number=number,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with account number: {number} does not exist")
        
        # maybe needed for unique ids?   
        id_note_database = str(uuid.uuid4())
        
        # insert to database
        create_note = accountNote.AccountNote(
            id = id_note_database,
            note = request_body.note, 
            # # accountNumber = generate_account_number.generate_id(),
            # accountNumber = number,

            # **vars(request_body), 

            accountId = user.first().id
        )
        db.add(create_note)
            
        db.commit()    
        db.refresh(create_note)
            
        return create_note
    
    def get_note(self, accountNumber, db: Session):
        
        user = account_repository.find_note(
            number=accountNumber,
            db=db
        )
        
        return user
    
    def update_note(self, id, account_request : UpdateNoteRequestDTO, 
                        db: Session):
        user = account_repository.find_note_by_id(
            id=id,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Note with id: {id} does not exist")
            
        update_data = {**vars(account_request)}
        
        user.update(update_data, synchronize_session=False)
        db.commit()
        
        return user.first()
    
    def delete_note(self, id, db: Session):
        
        user = account_repository.find_note_by_id(
            id=id,
            db=db
        )
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Note with id: {id} does not exist")
            
        
        user.delete(synchronize_session=False)
        db.commit()

        return {"message": f"Deleted {id} successfully"}