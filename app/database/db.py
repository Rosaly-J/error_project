from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from config.settings import Settings
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# settings.DATABASE_URL을 사용해 PostgreSQL 연결 URL 설정
settings = Settings()
engine = create_async_engine(
    settings.database_url,  # .env 파일에서 불러온 PostgreSQL 연결 URL
)

# AsyncSessionLocal 설정
AsyncSessionLocal = async_sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

# 메타데이터와 모델 네이밍 규칙 설정
naming_convention = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

# .env 파일에서 환경 변수 로드
load_dotenv()

# 데이터베이스 URL 환경 변수에서 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 의존성으로 사용할 DB 세션 생성 함수
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base 정의
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))

class ExampleModel(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    name = Column(String)
