from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from sqlalchemy.orm import Session
# from typing import Optional, List


try:
    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    print("Database connection succesfull !!!")

except Exception as error:
      
      print("Connecting to database failed !!!")
      print("Error: ", error)


sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


#connecting the database with psycopg2(postgress driver)  
# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#     password='12345678', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("DataBase Connection Succesfull !!!")
# except Exception as error:
#     print("Connecting to database failed !!!")
#     print("Error: ", error)