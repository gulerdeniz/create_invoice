# → veritabanı işlemleri
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
url = "sqlite:///./faturalar.db"

engine = create_engine(url)
local_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()