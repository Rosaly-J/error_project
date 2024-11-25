from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from datetime import datetime
from app.database.db import Base
import uuid

# 비동기 엔진 설정
DATABASE_URL = "postgresql+asyncpg://hwi:1234@localhost/voca"
engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kakao_id = Column(Integer, unique=True, nullable=False)  # 카카오 고유 ID
    email = Column(String, unique=True, nullable=True)      # 이메일 (카카오 계정)
    nickname = Column(String, nullable=False)               # 닉네임
    password = Column(String, nullable=True)               # 쇼설 로그인이라 이쪽에서 관리 안해서 nullable=True
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")  # 생성 날짜

    search_histories = relationship("SearchHistory", back_populates="user")


class SearchHistory(Base):
    __tablename__ = "search_history"
    __table_args__ = {'extend_existing': True}

    search_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True)  # ForeignKey로 관계 설정
    search_term = Column(String(255), index=True)
    search_date = Column(DateTime, default=datetime.utcnow)
    notification_id = Column(UUID(as_uuid=True), default=uuid.uuid4)

    # 관계 설정
    user = relationship("User", back_populates="search_histories")
