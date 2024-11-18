from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    kakao_id = Column(String, unique=True, nullable=False)  # 카카오 고유 ID
    email = Column(String, unique=True, nullable=True)      # 이메일 (카카오 계정)
    nickname = Column(String, nullable=True)               # 닉네임
