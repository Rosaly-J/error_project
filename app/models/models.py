from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# 비동기 엔진 설정
DATABASE_URL = "postgresql+asyncpg://hwi:1234@localhost/voca"
engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kakao_id = Column(Integer, unique=True, nullable=False)  # 카카오 고유 ID
    email = Column(String, unique=True, nullable=True)      # 이메일 (카카오 계정)
    nickname = Column(String, nullable=False)               # 닉네임
    password = Column(String, nullable=True)               # 쇼설 로그인이라 이쪽에서 관리 안해서 nullable=True
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")  # 생성 날짜

# 테이블 생성 함수
async def create_tables():
    async with engine.begin() as conn:
        # 테이블 생성
        await conn.run_sync(Base.metadata.create_all)

# FastAPI 애플리케이션에서 서버 실행 시 테이블을 생성하는 코드 추가
import asyncio

async def startup():
    await create_tables()

# 서버 실행 시 호출되도록 FastAPI에 통합 예시
from fastapi import FastAPI

app = FastAPI(on_startup=[startup])  # 서버 시작 시 테이블 생성
