from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core import security
from app.models.user import Token, User, TokenData
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
    },
    "sensor": {
        "username": "sensor",
        "full_name": "Portal Sensor Agent",
        "email": "sensor@example.com",
        "hashed_password": security.get_password_hash("sensor2026"),
        "role": "sensor",
        "is_active": True,
        "id": "2"
    },
    "soc": {
        "username": "soc",
        "full_name": "SOC Analyst",
        "email": "soc@example.com",
        "hashed_password": security.get_password_hash("soc2026"),
        "role": "soc",
        "is_active": True,
        "id": "3"
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
        data={"sub": user_dict["username"], "role": user_dict["role"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/live-login", response_model=Token)
async def live_login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login route used by push-ingestion middleware to emit real-time auth telemetry."""
    return await login_for_access_token(form_data)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.decode_access_token(token)
    if not payload:
        raise credentials_exception

    username: str | None = payload.get("sub")
    role: str | None = payload.get("role")
    token_data = TokenData(username=username, role=role)

    if not token_data.username:
        raise credentials_exception
    user = FAKE_USERS_DB.get(token_data.username)
    if not user:
        raise credentials_exception
    return user


def require_roles(*roles: str):
    async def _checker(user: dict = Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of roles: {', '.join(roles)}",
            )
        return user

    return _checker


@router.get("/me", response_model=User)
async def read_users_me(user: dict = Depends(get_current_user)):
    return user
