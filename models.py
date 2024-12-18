from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base



# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)  # Specify length
    role = Column(String(50), default="customer")  # Specify length
    subscription_plan_id = Column(Integer, ForeignKey("subscription_plans.id"))

    # Relationship with SubscriptionPlan
    subscription_plan = relationship("SubscriptionPlan", back_populates="users")

# Subscription Plan Model
class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)  # Specify length
    description = Column(String(255))  # Specify length
    permissions = Column(String(255))  # Specify length for comma-separated permissions
    limits = Column(Integer)  # Integer for API call limits

    # Relationship with User
    users = relationship("User", back_populates="subscription_plan")


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    api_endpoint = Column(String(255))
    description = Column(String(255))


class Usage(Base):
    __tablename__ = "usages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_name = Column(String(100))
    request_count = Column(Integer, default=0)

    # Relationship with User
    user = relationship("User")