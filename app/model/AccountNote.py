import uuid
from sqlalchemy import Column, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from config.database import Base

CUSTOMER_ACC = "CustomerAccount"

class AccountNote(Base):
    __tablename__ = 'account_notes'
    
    id: Mapped[str] = Column(String, primary_key=True, nullable=False, default=str(uuid.uuid4()))
    note: Mapped[str] = Column(String, nullable=True)

    # accountNumber: Mapped[str] = Column(String, nullable=True)
    
    # # Define the one-to-one relationship with CustomerAccount
    # accountId : Mapped[str] = Column(String, ForeignKey('account_customer.id'), nullable=False)
    # account: Mapped[CUSTOMER_ACC] = relationship(
    #     "CustomerAccount",
    #     back_populates="additionalDetails",
    #     cascade="all"
    # )

    # Define the many-to-one relationship with CustomerKYC
    accountId : Mapped[str] = Column(String, ForeignKey('account_customer.id'), nullable=False)
    account: Mapped[CUSTOMER_ACC] = relationship(
        "CustomerAccount", 
        back_populates="accountNote",
        cascade="all"
    )

    # @ManyToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    # @JoinColumn(name = "account_id")
    # @JsonIgnore
    # private Account account;
    
    def __repr__(self):
        return f"<AccountNote {self.id}>"