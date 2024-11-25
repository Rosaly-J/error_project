from fastapi import APIRouter, Body, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from requests import Session
from database.db import get_db
from models.models import SearchHistory as SearchHistoryDB, SearchHistory

router = APIRouter()

# 과거 검색 기록 (예제 데이터를 위한 임시 저장소)
search_history = ["apple", "application", "banana", "band", "cat", "dog"]

# 입력 데이터 모델
class SuggestRequest(BaseModel):
    query: str = Field(..., min_length=1, pattern="^[a-zA-Z]+$")  # 'regex' 대신 'pattern' 사용

# 출력 데이터 모델
class SuggestResponse(BaseModel):
    suggestions: List[str]

# /search/suggest 엔드포인트 구현
@router.post("/search/suggest", response_model=SuggestResponse)
async def suggest_words(request: SuggestRequest = Body(...)):
    query = request.query.lower()

    # 과거 검색 기록에서 자동 완성 제안
    suggestions = [word for word in search_history if word.startswith(query)]

    # 제안이 없으면 빈 배열 반환
    return {"suggestions": suggestions}


@router.get("/search/history", response_model=List[SearchHistory])
async def get_search_history(user_id: int, limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    search_history = db.query(SearchHistoryDB).filter(SearchHistoryDB.user_id == user_id).offset(skip).limit(
        limit).all()
    if not search_history:
        raise HTTPException(status_code=404, detail="No search history found")
    return search_history


@router.delete("/search/history", response_model=dict)
async def delete_search_history(user_id: int, search_term: str = None, db: Session = Depends(get_db)):
    query = db.query(SearchHistoryDB).filter(SearchHistoryDB.user_id == user_id)

    if search_term:
        # 특정 검색어 삭제
        query = query.filter(SearchHistoryDB.search_term == search_term)

    deleted_count = query.delete()
    db.commit()

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="No search history found to delete")

    return {"message": "Search history deleted successfully"}

