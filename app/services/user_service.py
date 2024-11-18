from sqlalchemy.orm import Session
from app.models.models import User

def get_user_by_kakao_id(db: Session, kakao_id: str):
    """카카오 ID로 사용자 조회"""
    return db.query(User).filter(User.kakao_id == kakao_id).first()

def create_user(db: Session, user_data: dict):
    """사용자 생성"""
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
