from __future__ import annotations
import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Enum, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PaymentStatus(str, enum.Enum):
    """
    Enumeration of possible payment statuses.
    
    Attributes:
        PENDING: Payment is pending.
        COMPLETED: Payment is completed successfully.
        FAILED: Payment has failed.
    """
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Payment(Base):
    """
    SQLAlchemy model for the 'payments' table.
    
    Attributes:
        id (int): Unique identifier for the payment.
        amount (float): Amount of the payment.
        status (PaymentStatus): Status of the payment.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Update timestamp.
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class PaymentBase(BaseModel):
    """
    Pydantic base model for payment attributes.
    
    Attributes:
        amount (float): Amount of the payment (must be greater than 0).
        status (PaymentStatus): Status of the payment.
    """
    amount: float = Field(..., gt=0, description="Total amount for the payment.")
    status: PaymentStatus = Field(PaymentStatus.PENDING, description="Current status of the payment.")


class PaymentCreate(PaymentBase):
    """
    Pydantic model for creating a new payment record.
    
    Extends:
        PaymentBase: Base payment attributes.
    """
    # TODO: Implement additional fields or custom logic for creation if necessary.
    pass


class PaymentUpdate(BaseModel):
    """
    Pydantic model for updating an existing payment record.
    
    Attributes:
        amount (Optional[float]): Updated amount of the payment.
        status (Optional[PaymentStatus]): Updated status of the payment.
    """
    amount: Optional[float] = Field(None, gt=0, description="Updated amount for the payment.")
    status: Optional[PaymentStatus] = Field(None, description="Updated status of the payment.")


class PaymentInDBBase(PaymentBase):
    """
    Base Pydantic model for payment data in the database.
    
    Attributes:
        id (int): Unique identifier of the payment.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Update timestamp.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PaymentInDB(PaymentInDBBase):
    """
    Pydantic model representing the payment as stored in the database.
    
    Extends:
        PaymentInDBBase
    """
    pass


class PaymentResponse(PaymentInDBBase):
    """
    Pydantic model for returning payment data in responses.
    
    Extends:
        PaymentInDBBase
    """
    # TODO: Add any necessary fields or methods for response scenarios.
    pass