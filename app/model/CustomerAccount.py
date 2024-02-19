import uuid
from sqlalchemy import Column, String, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship
from config.database import Base
from model.enum.CustomerStatusType import CustomerStatusType
from model.enum.AccountType import AccountType
from typing import List, Optional

ADDITIONAL_DETAIL = "AccountAdditionalDetails"
CUSTOMER = "CustomerKYC"
CUSTOMER_NOTE = "AccountNote"

class CustomerAccount(Base):
    __tablename__ = 'account_customer'
    
    id: Mapped[str] = Column(String, primary_key=True, nullable=False, default=str(uuid.uuid4()))
    accountName: Mapped[str] = Column(String, nullable=False)
    accountNumber: Mapped[str] = Column(String, nullable=False)
    stakeholderIds: Mapped[str] = Column(String, nullable=False)
    status: Mapped[CustomerStatusType] = Column(String, nullable=False)
    type : Mapped[AccountType] = Column(String, nullable=False)
    openingTimestamp : Mapped[DateTime] = Column(DateTime, nullable=True)
    closingTimestamp : Mapped[DateTime] = Column(DateTime, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('accountNumber', name='unique_customer_account_1'),
    )
    # Define the one-to-one relationship with AccountAdditionalDetails
    additionalDetails: Mapped[ADDITIONAL_DETAIL] = relationship(
        "AccountAdditionalDetails", 
        back_populates="account",
        cascade="all"
    )
    
    # Define the many-to-one relationship with CustomerKYC
    customerId : Mapped[str] = Column(String, ForeignKey('customer_kyc.id'), nullable=False)
    customer: Mapped[CUSTOMER] = relationship(
        "CustomerKYC", 
        back_populates="accounts",
        cascade="all"
    )

    # Define the one-to-many relationship with CustomerAccount
    accountNote: Mapped[List[CUSTOMER_NOTE] | None] = relationship(
            "AccountNote", 
            back_populates="account",
            cascade="all"
        )

    def __repr__(self):
        return f"<CustomerAccount {self.id}, {self.accountNumber}>"