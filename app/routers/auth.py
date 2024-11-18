from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.kakao_oauth import KakaoOAuthService, get_kakao_service
from app.services.user_service import get_user_by_kakao_id, create_user
from app.database.db import get_db  # SQLAlchemy 세션 가져오는 함수
from app.utils.utils import create_jwt_token  # JWT 발급 함수

router = APIRouter()

# 카카오 로그인 URL 반환
@router.get("/auth/kakao")
async def kakao_login(service: KakaoOAuthService = Depends(get_kakao_service)):
    login_url = service.get_login_url()
    return {"login_url": login_url}

# 카카오 인증 후 콜백 처리
@router.get("/auth/kakao/callback")
async def kakao_callback(code: str = Query(...), service: KakaoOAuthService = Depends(get_kakao_service)):
    try:
        # Access Token 발급
        access_token = await service.get_access_token(code)

        # 사용자 정보 가져오기
        user_info = await service.get_user_info(access_token)
        kakao_id = user_info["id"]
        email = user_info["kakao_account"]["email"]
        nickname = user_info.get("properties", {}).get("nickname")

        # 데이터베이스에서 사용자 조회
        user = get_user_by_kakao_id(get_db, kakao_id)
        if not user:
            # 신규 사용자면 회원가입 처리
            user_data = {
                "kakao_id": kakao_id,
                "email": email,
                "nickname": nickname,
            }
            user = create_user(get_db, user_data)

        # JWT 발급
        token = create_jwt_token({"user_id": user.id, "kakao_id": user.kakao_id})
        return {"message": "Login successful", "access_token": token}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {e}")
