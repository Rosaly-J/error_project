from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.kakao_oauth import KakaoOAuthService, get_kakao_service
from app.services.user_service import get_user_by_kakao_id, create_user
from app.database.db import get_db  # SQLAlchemy 세션 가져오는 함수
from app.utils.utils import create_jwt_token  # JWT 발급 함수
from app.models.models import User

router = APIRouter()

# 카카오 로그인 URL 반환
@router.get("/auth/kakao")
async def kakao_login(service: KakaoOAuthService = Depends(get_kakao_service)):
    login_url = service.get_login_url()
    return {"login_url": login_url}

# 카카오 인증 후 콜백 처리
@router.get("/auth/kakao/callback")
async def kakao_callback(
    code: str = Query(...),
    service: KakaoOAuthService = Depends(get_kakao_service),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Access Token 발급
        print(f"Received code: {code}")
        print(f"Service: {service}")
        access_token = await service.get_access_token(code)

        # 사용자 정보 가져오기
        user_info = await service.get_user_info(access_token)
        kakao_id = user_info["id"]
        email = user_info["kakao_account"]["email"]
        nickname = user_info.get("properties", {}).get("nickname")

        # 데이터베이스에서 사용자 조회
        query = select(User).filter(User.kakao_id == kakao_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            # 신규 사용자면 회원가입 처리
            user_data = {
                "kakao_id": kakao_id,
                "email": email,
                "nickname": nickname,
                "password": None,
            }
            user = await create_user(db, user_data)

        # JWT 발급
        token = create_jwt_token({"user_id": user.id, "kakao_id": user.kakao_id})
        return {"message": "Login successful", "access_token": token}

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key in user info: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")