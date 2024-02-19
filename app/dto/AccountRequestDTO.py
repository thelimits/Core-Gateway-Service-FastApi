from pydantic import BaseModel, validator
from typing import List, Optional

class InstanceParamSavingAccountDTO(BaseModel):
    accountTierNames: str
    interestApplicationDay: str = "1"
    inactivityFeeApplicationDay: str = "1"
    maintenanceFeeApplicationDay: str = "1"
    dailyWithdrawalLimitByTransactionType: float = 50000000
    
class InstanceParamLoanDTO(BaseModel):
    fixedInterestRate: float = 0.1
    upfrontFee: float = 0.00
    amortiseUpfrontFee: str = "False"
    fixedInterestLoan: str = "True"
    totalTerm: int = 12
    principal: float = 1000000.00
    repaymentDay: int = 28
    depositAccount: str
    variableRateAdjustment: float = 0.00
    interestAccrualRestType: str = "daily"
    capitaliseLateRepaymentFee: str = "False"
    repaymentHolidayImpactPreference: str = "increase_emi"
    
    # if loan account with balloon payment
    amortisationMethodNoBalloon: Optional[str] = "declining_principal"
    amortisationMethodWithBalloon: Optional[str] = "minimum_repayment_with_balloon_payment"
    balloonPaymentAmount: Optional[float] = None
    balloonPaymentDaysDelta: Optional[int] = None
    
class AccountAdditionalDetailsDTO(BaseModel):
    sourceOfFunds: Optional[str] = None
    workPlace: Optional[str] = None
    rangeSalaries: Optional[str] = None
    purpose: Optional[str] = None
    
class CreateAccountRequestDTO(BaseModel):
    productVersionId: str
    baseCurrency: Optional[str] = None
    accountName: str
    instanceParameter: Optional[InstanceParamSavingAccountDTO] = None
    InstanceParamLoan: Optional[InstanceParamLoanDTO] = None
    accountAdditionalDetails: Optional[AccountAdditionalDetailsDTO] = None

class CreateNoteRequestDTO(BaseModel):
    note: str

class UpdateNoteRequestDTO(BaseModel):
    note: str