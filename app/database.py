import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
#     "<database>://<username>:<password>@<ip-address/hostname>/<database_name>"
# )
database = os.getenv("DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
hostname = os.getenv("DB_HOSTNAME")
database_name = os.getenv("DB_NAME")
SQLACHEMY_DATABASE_URL = "{0}://{1}:{2}@{3}/{4}".format(
    database, username, password, hostname, database_name
)

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
