from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# TODO: Replace this with your project's base class import if needed
Base = declarative_base()


class Subscription(Base):
    """
    SQLAlchemy model for subscription data.
    Represents a subscription record in the database.
    """
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # TODO: Consider adding billing_cycle, next_billing_date, or other fields


class SubscriptionBase(BaseModel):
    """
    Base Pydantic model for subscription data.
    Includes common fields shared by different subscription operations.
    """
    plan_type: str
    is_active: Optional[bool] = True


class SubscriptionCreate(SubscriptionBase):
    """
    Pydantic model for creating a subscription.
    Includes fields required during creation.
    """
    user_id: int


class SubscriptionUpdate(BaseModel):
    """
    Pydantic model for updating a subscription.
    Fields are optional because they may or may not be updated.
    """
    plan_type: Optional[str]
    is_active: Optional[bool]


class SubscriptionRead(SubscriptionBase):
    """
    Pydantic model for reading a subscription.
    Includes read-only fields.
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enables ORM compatibility for SQLAlchemy models

    # TODO: Add additional fields that are relevant to read-only operations if necessary