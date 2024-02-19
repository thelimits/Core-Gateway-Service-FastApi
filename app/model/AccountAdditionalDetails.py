import uuid
from sqlalchemy import Column, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from config.database import Base

CUSTOMER_ACC = "CustomerAccount"

class AccountAdditionalDetails(Base):
    __tablename__ = 'account_additional_details'
    
    id: Mapped[str] = Column(String, primary_key=True, nullable=False, default=str(uuid.uuid4()))
    sourceOfFunds: Mapped[str] = Column(String, nullable=True)
    workPlace: Mapped[str] = Column(String, nullable=True)
    rangeSalaries: Mapped[str] = Column(String, nullable=True)
    purpose: Mapped[str] = Column(String, nullable=True)
    
    # Define the one-to-one relationship with CustomerAccount
    accountId : Mapped[str] = Column(String, ForeignKey('account_customer.id'), nullable=False)
    account: Mapped[CUSTOMER_ACC] = relationship(
        "CustomerAccount",
        back_populates="additionalDetails",
        cascade="all"
    )
    
    def __repr__(self):
        return f"<AccountAdditionalDetails {self.id}>"