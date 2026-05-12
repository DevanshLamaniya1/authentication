from fastapi import status , HTTPException  , Depends
from authentication.jwt_creation import oauth , check_jwt
from sqlalchemy.orm import Session
from db.db import get_db
from models.user_model import User


def get_current_user(token : str = Depends(oauth) , db : Session = Depends(get_db)):

    payload = check_jwt(token)
    
    user_id = payload.get("id")

    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , "user id is not available")
    
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , "user is not authenticated")
    
    return user_id