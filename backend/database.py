from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://uname:pswd@localhost/db"

engine = create_engine(DATABASE_URL)
base = declarative_base()
SessionLocal = sessionmaker(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()