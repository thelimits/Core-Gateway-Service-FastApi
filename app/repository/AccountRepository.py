import math
from sqlalchemy import desc, asc, func, or_
from sqlalchemy.orm import Session, joinedload
from dto.CustomerResponseDTO import CustomerResponseDTO, CustomerResponseWithAccountDTO
from dto.CustomerResponseDTO import CustomerPageResponseDTO
import model.CustomerKYC as model_cust
import model.CustomerAccount as model_acc
import model.AccountNote as model_note
from dto.AccountResponseDTO import AccountResponseDTO

class AccountRepository:
    def __init__(self) -> None:
        pass

    @staticmethod
    def find_account_by_id_customer(id: str, db: Session):

        query = db.query(model_cust.CustomerKYC).options(joinedload(model_cust.CustomerKYC.accounts).joinedload(model_acc.CustomerAccount.accountNote)).options(joinedload(model_cust.CustomerKYC.accounts).joinedload(model_acc.CustomerAccount.additionalDetails)).filter(
            model_cust.CustomerKYC.id == id
        )
        
        return query
    
    @staticmethod
    def find_customer_by_account_number(number: str, db: Session):
        query = db.query(model_cust.CustomerKYC).options(joinedload(model_cust.CustomerKYC.accounts).joinedload(model_acc.CustomerAccount.accountNote)).options(joinedload(model_cust.CustomerKYC.accounts).joinedload(model_acc.CustomerAccount.additionalDetails)).filter(
            model_acc.CustomerAccount.accountNumber == number
        ).join(model_acc.CustomerAccount)
        
        return query
    
    @staticmethod
    def find_by_account_number(number: str, db: Session):
        query = db.query(model_acc.CustomerAccount).filter(
            model_acc.CustomerAccount.accountNumber == number
        )
        
        return query
    
    @staticmethod
    def find_note(number: str, db: Session):
        query = db.query(model_acc.CustomerAccount).options(joinedload(model_acc.CustomerAccount.accountNote)).filter(
            model_acc.CustomerAccount.accountNumber == number
        ).first()
        
        return query
    
    @staticmethod
    def find_note_by_id(id: str, db: Session):
        query = db.query(model_note.AccountNote).filter(
            model_note.AccountNote.id == id
        )
        
        return query
    
    @staticmethod
    def search_customer_by_name_and_account_type(sort_by: str,
        sort_order: str,
        column_mapping: dict(),
        filter: dict(),
        db: Session):
        
        sorting_column = column_mapping[sort_by]
        sorting_column = desc(sorting_column) if sort_order == "desc" else asc(sorting_column)
        
        query = db.query(model_cust.CustomerKYC).options(joinedload(model_cust.CustomerKYC.accounts).joinedload(model_acc.CustomerAccount.accountNote)).options(joinedload(model_cust.CustomerKYC.accounts).joinedload(model_acc.CustomerAccount.additionalDetails)).filter(
            or_(filter['status'] is None, model_cust.CustomerKYC.status == func.upper(filter['status'])),
                        func.concat(func.upper(model_cust.CustomerKYC.firstName),
            ' ',
            func.upper(model_cust.CustomerKYC.lastName)).ilike(
                func.concat('%', func.upper(filter['q']), '%')
            )
        ).order_by(sorting_column)

        # Hitung jumlah total data yang sesuai dengan filter
        total_record = query.count()
        
        # Pagination
        offset_page = (filter['page'] - 1) * filter['size']
        
        # Hitung total halaman
        total_page = math.ceil(total_record / filter['size'])
        
        all_customer = query.offset(offset_page).limit(filter['size']).all()
        
        return all_customer