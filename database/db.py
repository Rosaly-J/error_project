from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from config.settings import Settings
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# settings.DATABASE_URL을 사용해 PostgreSQL 연결 URL 설정
settings = Settings()
print(settings.database_url)
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

# Base 정의
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))

class ExampleModel(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    name = Column(String)
