import asyncio

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker, async_session,
)
from sqlalchemy.orm import declarative_base
from config.settings import Settings
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# settings.DATABASE_URL을 사용해 PostgreSQL 연결 URL 설정
settings = Settings()
SQLALCHEMY_DATABASE_URL = os.getenv("postgresql+asyncpg://hwi:1234@localhost/voca", settings.database_url)

# 비동기 엔진 생성
engine = create_async_engine(
    "postgresql+asyncpg://hwi:1234@localhost/voca",  # .env 파일에서 불러온 PostgreSQL 연결 URL
    echo=True,
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

# 세션 생성
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 의존성으로 사용할 DB 세션 생성 함수
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Base 정의
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))

# 테이블 생성 함수
async def create_tables():
    async with engine.begin() as conn:
        # 테이블 생성
        await conn.run_sync(Base.metadata.create_all)

# 테이블 생성 호출
if __name__ == "__main__":
    asyncio.run(create_tables())  # 테이블 생성


class ExampleModel(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    name = Column(String)
