from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from app import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login" )

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={ "WWw-Authenticate": "Bearer"},
    )

    return token.verify_token(data, credentials_exception)

