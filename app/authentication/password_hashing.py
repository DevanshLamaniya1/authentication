import bcrypt

def create_password(password:str):

    if password is None:
        raise ValueError("the password cannot be none.")
    
    hashed_pw = bcrypt.hashpw(password.encode("utf-8") , bcrypt.gensalt())

    return hashed_pw.decode("utf-8")

def check_password(entered_pass:str,hashed_pass:str):

    entered_pass = entered_pass.encode("utf-8")
    hashed_pass = hashed_pass.encode("utf-8")

    result = bcrypt.checkpw(entered_pass , hashed_pass)

    return result

# print(create_password("devansh@123"))

# print(check_password("devansh@125","$2b$12$1Ul2e498aARHZZG2hNl32un0wBTWX9o8z2.yNNnmJpraffwWZMIti"))