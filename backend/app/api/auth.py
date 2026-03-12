from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core import security
from app.models.user import Token, User, UserInDB
from datetime import timedelta

router = APIRouter()

# Mock user database for prototype
FAKE_USERS_DB = {
    "abdul": {
        "username": "abdul",
        "full_name": "Abdul Sammed Shaik",
        "email": "abdul@example.com",
        "hashed_password": security.get_password_hash("sentinela2026"),
        "role": "admin",
        "is_active": True,
        "id": "1"
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = FAKE_USERS_DB.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not security.verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    # In a real app, we would decode token and fetch user from DB
    # For prototype, we'll assume 'abdul' for any valid token logic
    return FAKE_USERS_DB["abdul"]
