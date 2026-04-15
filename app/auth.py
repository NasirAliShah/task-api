from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_database
from app.security import SecurityUtils
from app.user_crud import get_user_by_email
from app.exceptions import UnauthorizedException
from app.logger import logger

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_database)):
    token = credentials.credentials
    payload = SecurityUtils.decode_token(token)
    
    if payload is None:
        logger.warning(f"Invalid token attempt")
        raise UnauthorizedException("Invalid authentication credentials")
    
    email: str = payload.get("sub")
    if email is None:
        logger.warning(f"Token missing email claim")
        raise UnauthorizedException("Invalid token")
    
    user = await get_user_by_email(db, email)
    if user is None:
        logger.warning(f"User not found for email: {email}")
        raise UnauthorizedException("User not found")
    
    logger.debug(f"User authenticated: {email}")
    return user
