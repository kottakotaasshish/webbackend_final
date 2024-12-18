from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User

router = APIRouter()

# Pydantic model for login
class LoginModel(BaseModel):
    username: str
    password: str

# JWT configuration
class Settings(BaseModel):
    authjwt_secret_key: str = "your_secret_key"  # Replace with your secret key

@AuthJWT.load_config
def get_config():
    return Settings()

# Login endpoint
@router.post("/login")
def login(login: LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # For simplicity, checking password directly. Replace with hashed password verification.
    if login.password != "password123":
        raise HTTPException(status_code=401, detail="Invalid password")

    # Generate access token
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token, "role": user.role}
