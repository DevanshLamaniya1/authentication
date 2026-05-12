from pydantic import BaseModel , EmailStr , field_validator , Field
import re
from typing import Annotated

class CreateUser(BaseModel):
    user_name : Annotated[str , Field(... , examples=["User name"])]
    user_email : Annotated[str , Field(... , examples=["User email"])]
    password : Annotated[str , Field(... , min_length=8 , description="User@123")]

    @field_validator("password")
    def strong_password(password):
        if not re.search(r"[A-Z]", password):
            raise ValueError("password must contain at least 1 upper case ")

        if not re.search(r"[a-z]", password):
            raise ValueError("password must contain at least 1 small case")

        if not re.search(r"\d" , password):
            raise ValueError("password must contain at least 1 digit")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>-]', password):
            raise ValueError("password must contain at least 1 special character")

        return password

    @field_validator("user_email")
    def email_only(user_email: str):

        if not user_email.lower().endswith("@gmail.com"):
            raise ValueError("only gamil address are allowed")

        return user_email