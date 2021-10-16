
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///db.db'
engine = create_engine( SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False} )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()