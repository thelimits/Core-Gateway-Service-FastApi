from sqlalchemy import Column, String, Date, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from config.database import Base
from sqlalchemy.orm import declared_attr
from typing import List, Optional

CUSTOMER_ACC = "CustomerAccount"

class DateAuditEntity(Base):
    __abstract__ = True
    
    @declared_attr
    def createdAt(cls):
        return Column(DateTime, default=func.now())
    
    @declared_attr
    def updatedAt(cls):
        return Column(DateTime, onupdate=func.now())
    
    @declared_attr
    def activatedAt(cls):
        return cls._create_activated_at_column()
    
    @classmethod
    def _create_activated_at_column(cls):
        return Column(DateTime)
    
    # @classmethod
    # def set_activation_time(cls):
    #     print(cls.status, CustomerStatusType.ACTIVE.value)
    #     return func.now() if cls.status is not None and cls.status != CustomerStatusType.ACTIVE.value else None
    
class CustomerKYC(DateAuditEntity):
    __tablename__ = 'customer_kyc'
    
    id: Mapped[str] = Column(String, primary_key=True, nullable=False)
    firstName: Mapped[str] = Column(String, nullable=False)
    lastName: Mapped[str] = Column(String, nullable=False)
    address: Mapped[str] = Column(String, nullable=False)
    nik: Mapped[str] = Column(String, nullable=False)
    dob: Mapped[Date] = Column(Date, nullable=False)
    motherMaidenName: Mapped[str] = Column(String, nullable=False)
    email: Mapped[str] = Column(String, nullable=False)
    pin: Mapped[str] = Column(String, nullable=False)
    phoneNumber: Mapped[str] = Column(String, nullable=False)
    status: Mapped[str] = Column(String, nullable=False)
    
    # Define the one-to-many relationship with CustomerAccount
    accounts: Mapped[List[CUSTOMER_ACC] | None] = relationship(
            "CustomerAccount", 
            back_populates="customer",
            cascade="all"
        )
    
    __table_args__ = (
        UniqueConstraint('phoneNumber', 'email', 'nik', name='unique_customer_kyc_1'),
    )
    
    def __repr__(self):
        return f"<CustomerKYC {self.id}>"