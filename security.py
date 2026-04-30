from fastapi import  Request, Depends, HTTPException, status, Header
from jose import jwt, JWTError
from database import SessionLocal
import os
from sqlalchemy.orm import Session
import models

def get_token_from_request(request: Request):

    # from auth header cli
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    
    # from the cookie (web portal)
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token
    
    # if neither exists, block access
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated. Please log in"
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_active_user(token: str = Depends(get_token_from_request), 
    db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Check if the user exists in the database
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account suspended.")
    
    return user

# --- Role-Based Access Control (RBAC) ---
def require_admin(current_user: models.User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return current_user

def verify_api_version(x_api_version: str = Header(default=None)):
    if x_api_version is None:
        raise HTTPException(status_code=400, detail="Missing X-API-Version header. Please specify version.")
        
    if x_api_version != "1":
        raise HTTPException(status_code=400, detail=f"Unsupported API Version: {x_api_version}. Expected '1'.")
        
    return x_api_version
