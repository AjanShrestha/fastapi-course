import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# while True:
#     try:
#         conn = psycopg.connect(
#             "host=<hostname> dbname=<dbname> user=<username> password=<password>",
#             row_factory=dict_row,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: %s" % error)
#         time.sleep(2)


# connection string
# SQLACHEMY_DATABASE_URL = (
#     "<database>://<username>:<password>@<ip-address/hostname>:<port>/<database_name>"
# )
SQLACHEMY_DATABASE_URL = f"{settings.database}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# engine - responsible for SQLAlchemy to connect to the database
engine = create_engine(SQLACHEMY_DATABASE_URL)

# talk to the database via session
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# base class - all of the models that we define to create tables
# extends this base class
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
