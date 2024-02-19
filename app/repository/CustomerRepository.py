import math
from sqlalchemy import desc, asc, func, or_
from sqlalchemy.orm import Session, joinedload
from dto.CustomerResponseDTO import CustomerResponseDTO
from dto.CustomerResponseDTO import CustomerPageResponseDTO
import model.CustomerKYC as model

class CustomerRepository:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_all_customers(
        sort_by: str,
        sort_order: str,
        column_mapping: dict(),
        filter: dict(),
        db: Session
        ):
        
        sorting_column = column_mapping[sort_by]
        sorting_column = desc(sorting_column) if sort_order == "desc" else asc(sorting_column)
        
        query = db.query(model.CustomerKYC).filter(
            model.CustomerKYC.status == filter['status'].upper()
        ).order_by(sorting_column)

        # Hitung jumlah total data yang sesuai dengan filter
        total_record = query.count()
        
        # Pagination
        offset_page = (filter['page'] - 1) * filter['size']
        
        # Hitung total halaman
        total_page = math.ceil(total_record / filter['size'])
        
        all_customer = query.offset(offset_page).limit(filter['size']).all()
    
        customer_dtos = [
            CustomerResponseDTO(
                **vars(record)
            )
            for record in all_customer
        ]
    
        return CustomerPageResponseDTO(
            page_number=filter['page'],
            page_size=filter['size'],
            total_pages=total_page,
            total_record=total_record,
            customers=customer_dtos
        )
    
    @staticmethod
    def get_customer_by_id(id: str, db: Session):
        customer = db.query(model.CustomerKYC).filter(
            model.CustomerKYC.id == id
        )
        
        return customer
    
    @staticmethod
    def get_customer_by_phone_number(phoneNumber: str, db: Session):
        customer = db.query(model.CustomerKYC).filter(
            model.CustomerKYC.phoneNumber == phoneNumber
        ).first()
        
        return customer
    
    @staticmethod
    def search_customer_by_name(sort_by: str,
        sort_order: str,
        column_mapping: dict(),
        filter: dict(),
        db: Session):
        
        sorting_column = column_mapping[sort_by]
        sorting_column = desc(sorting_column) if sort_order == "desc" else asc(sorting_column)
        
        query = db.query(model.CustomerKYC).filter(
            or_(filter['status'] is None, model.CustomerKYC.status == func.upper(filter['status'])),
            func.concat(func.upper(model.CustomerKYC.firstName),
                        ' ',
                        func.upper(model.CustomerKYC.lastName)).ilike(
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
        
        customer_dtos = [
            CustomerResponseDTO(
                **vars(record)
            )
            for record in all_customer
        ]
        
        return CustomerPageResponseDTO(
            page_number=filter['page'],
            page_size=filter['size'],
            total_pages=total_page,
            total_record=total_record,
            customers=customer_dtos
        )
    
    @staticmethod
    def search_customer_by_nik(
        sort_by: str,
        sort_order: str,
        column_mapping: dict(),
        filter: dict(),
        db: Session
        ):
        
        sorting_column = column_mapping[sort_by]
        sorting_column = desc(sorting_column) if sort_order == "desc" else asc(sorting_column)

        query = db.query(model.CustomerKYC).filter(
            or_(filter['status'] is None, model.CustomerKYC.status == func.upper(filter['status'])),
            model.CustomerKYC.nik.like(f"%{filter['q']}%")
        ).order_by(sorting_column)
        
        # Hitung jumlah total data yang sesuai dengan filter
        total_record = query.count()
        
        # Pagination
        offset_page = (filter['page'] - 1) * filter['size']
        
        # Hitung total halaman
        total_page = math.ceil(total_record / filter['size'])
        
        all_customer = query.offset(offset_page).limit(filter['size']).all()
        
        customer_dtos = [
            CustomerResponseDTO(
                **vars(record)
            )
            for record in all_customer
        ]
        
        return CustomerPageResponseDTO(
            page_number=filter['page'],
            page_size=filter['size'],
            total_pages=total_page,
            total_record=total_record,
            customers=customer_dtos
        )
    
    @staticmethod
    def search_customer_by_phone(
        sort_by: str,
        sort_order: str,
        column_mapping: dict(),
        filter: dict(),
        db: Session
        ):
        
        sorting_column = column_mapping[sort_by]
        sorting_column = desc(sorting_column) if sort_order == "desc" else asc(sorting_column)

        query = db.query(model.CustomerKYC).filter(
            or_(filter['status'] is None, model.CustomerKYC.status == func.upper(filter['status'])),
            model.CustomerKYC.phoneNumber.like(f"%{filter['q']}%")
        ).order_by(sorting_column)
        
        # Hitung jumlah total data yang sesuai dengan filter
        total_record = query.count()
        
        # Pagination
        offset_page = (filter['page'] - 1) * filter['size']
        
        # Hitung total halaman
        total_page = math.ceil(total_record / filter['size'])
        
        all_customer = query.offset(offset_page).limit(filter['size']).all()
        
        customer_dtos = [
            CustomerResponseDTO(
                **vars(record)
            )
            for record in all_customer
        ]
        
        return CustomerPageResponseDTO(
            page_number=filter['page'],
            page_size=filter['size'],
            total_pages=total_page,
            total_record=total_record,
            customers=customer_dtos
        )
            