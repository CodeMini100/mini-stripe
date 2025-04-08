from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customer(Base):
    """
    SQLAlchemy model for storing customer data.
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    # TODO: Add additional fields as needed, e.g., address, phone, etc.


class CustomerBase(BaseModel):
    """
    Base Pydantic model with shared properties for customer data.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerCreate(CustomerBase):
    """
    Pydantic model for creating a new customer.
    """
    name: str
    email: EmailStr


class CustomerUpdate(CustomerBase):
    """
    Pydantic model for updating existing customer data.
    """
    # TODO: Adjust fields or validations as necessary
    pass


class CustomerInDB(CustomerBase):
    """
    Pydantic model for customer data as stored in the database.
    """
    id: int

    class Config:
        orm_mode = True


class CustomerRead(CustomerInDB):
    """
    Pydantic model for reading customer data.
    """
    # TODO: Add additional fields needed for API response
    pass