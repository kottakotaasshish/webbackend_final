from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from dotenv import load_dotenv
import os

# Configuration for JWT
class Settings(BaseModel):
    authjwt_secret_key: str = "your_secret_key"  # Replace with a secure key

@AuthJWT.load_config
def get_config():
    return Settings()

# Pydantic model for login
class LoginModel(BaseModel):
    username: str
    password: str

# Endpoint for user login
def login_user(login: LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # Find the user in the database
    user = db.query(User).filter(User.username == login.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # For simplicity, no password hash is checked here. In production, hash passwords!
    if login.password != "password123":  # Replace with actual password verification
        raise HTTPException(status_code=401, detail="Invalid password")

    # Create JWT tokens
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token, "role": user.role}

# Dependency: Verify JWT token and get the current user
def get_current_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    username = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Dependency: Restrict to admins only
def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
