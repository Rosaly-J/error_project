import jwt
from datetime import datetime, timedelta
import redis
from dotenv import load_dotenv
import os
from fastapi import HTTPException
from redis_set import get_redis_client

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    """JWT 토큰 생성"""
    expire = datetime.utcnow() + timedelta(days=1)  # 1일 유효기간
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

import logging

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 로그 레벨을 INFO로 설정
ch = logging.StreamHandler()  # 콘솔로 출력하기 위한 핸들러
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def delete_access_token(token: str):
    """Redis에서 엑세스 토큰 삭제"""
    try:

        redis_client = get_redis_client()  # Redis 클라이언트 가져오기
        result = redis_client.delete(f"access_token:{token}")

        if result == 0:
            # 유효하지 않은 토큰에 대해 401 응답
            raise HTTPException(status_code=401, detail="Invalid token")  # 401 상태 코드로 변경

        return {"message": "Logout successful"}

    except redis.exceptions.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")
    except HTTPException as e:
        raise e  # 이 예외는 그대로 전달
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")