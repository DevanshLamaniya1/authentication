import jwt
from fastapi import status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta , datetime

from dotenv import load_dotenv
import os

from fastapi.security import OAuth2PasswordBearer

oauth = OAuth2PasswordBearer("/router/login")

load_dotenv()

SECRET_KEY = os.getenv("secretKey")
expire_time = 90
ALGORITHM = "HS256"

def create_jwt(data:dict):

    data_to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=expire_time)

    data_to_encode.update({"exp":expire})

    jwt_token = jwt.encode(data_to_encode,SECRET_KEY , ALGORITHM)

    return jwt_token


# create_data = {
#     "name" : "deavnsh",
#     "password" : "devansh123"
# }
# print(create_jwt(create_data))

def check_jwt(token:str):

    try:
        payload = jwt.decode(token , SECRET_KEY ,ALGORITHM)
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , "token expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , "invalid token")

