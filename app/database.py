# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor
from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# create session to a db to run queries and close it when we're done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# code to connect to postgres db using python postgres driver
# and run SQL queries directly instead of using sqlalchemy

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", 
#                                 database="fastapi", 
#                                 user="postgres", 
#                                 password="qwerty345",
#                                 port=5433,
#                                 cursor_factory=RealDictCursor) # to give column names with the returned value
#         cursor = conn.cursor() # use to execute queries
#         print("DB connection was succesfull")
#         break
#     except Exception as error:
#         print("Connecting to DB failed.")
#         print(f"Error: {error}") 
#         time.sleep(2)