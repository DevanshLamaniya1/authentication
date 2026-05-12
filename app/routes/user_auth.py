from fastapi import status , HTTPException  ,APIRouter , Depends
from app.schema.user import CreateUser
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user_model import User
from app.authentication.password_hashing import create_password , check_password
from fastapi.security import OAuth2PasswordRequestForm
from app.authentication.jwt_creation import create_jwt , oauth


user_authentication = APIRouter(prefix="/router" , tags=["authentication"])

@user_authentication.post("/create_user")
def create_user(user : CreateUser , db : Session = Depends(get_db)):

    existing_user = db.query(User).filter(user.user_email == User.email).first()

    if existing_user:
        raise HTTPException(status.HTTP_302_FOUND , "the user already exists")
    
    hashed_password = create_password(user.password)

    new_user = User(name = user.user_name , email = user.user_email , password = hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id" : new_user.id,
        "name" : new_user.name,
        "email" : new_user.email
    }

@user_authentication.post("/login")
def login_user(db : Session = Depends(get_db) , form_data :OAuth2PasswordRequestForm = Depends()):

    existing_user = db.query(User).filter(User.email == form_data.username).first()

    if not existing_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND , "user not found")
    
    if not check_password(form_data.password , existing_user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , "the password is incorrect")
    
    jwt_token = create_jwt({
        "id" : existing_user.id,
        "email" : existing_user.email,
        "name" : existing_user.name
    }) 

    return {
        "access_token" : jwt_token,
        "type" : "bearer"
    }

@user_authentication.get("/all_users")
def get_all_users(db:Session = Depends(get_db) , token: str = Depends(oauth)):

    return db.query(User).all()

@user_authentication.get("/user_{id}")
def get_user_by_id(id : int , db : Session = Depends(get_db) , token : str = Depends(oauth)):
    return db.query(User).filter(id == User.id).first()