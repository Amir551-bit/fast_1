from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings



engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread":False
    }
)



Sessionmaker = sessionmaker(autoflush=False, bind=engine, autocommit=False)


Base = declarative_base() 



def get_db():
    db = Sessionmaker()

    try:
        yield db
    finally:
        db.close()