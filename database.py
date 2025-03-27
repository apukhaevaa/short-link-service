from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql
pymysql.install_as_MySQLdb()
import ssl

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://user1:88673120369@rc1d-mbbjmf9mfbpt4fik.mdb.yandexcloud.net:3306/db1"
    "?ssl_ca=/Users/admin/.mysql/root.crt"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()