from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)

local_session = sessionmaker(bind = engine , autoflush=False , autocommit = False)
Base = declarative_base()

def get_db():
    db = local_session()

    try:
        yield db

    finally:
        db.close()

    