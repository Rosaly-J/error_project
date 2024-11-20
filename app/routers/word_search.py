from fastapi import APIRouter, Query, HTTPException
import httpx

router = APIRouter()

# dictionaryapi.dev를 호출하여 단어 정보 가져오기
async def get_word_info(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 404:  # 단어를 찾을 수 없는 경우
            raise HTTPException(status_code=404, detail="Word not found")

        if response.status_code != 200:  # 다른 에러 처리
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from dictionary API: {response.text}",
            )

        return response.json()

# /search/word 엔드포인트 구현
@router.get("/search/word")
async def search_word(word: str = Query(..., description="The word to search for")):
    word_info = await get_word_info(word)

    # 필요한 정보 추출 (예: 정의, 발음, 품사, 유의어, 예문 등)
    definitions = word_info[0].get("meanings", [])

    word_details = {
        "word": word,
        "definitions": [
            {
                "part_of_speech": meaning.get("partOfSpeech", "Unknown"),
                "definitions": meaning.get("definitions", []),
            }
            for meaning in definitions
        ],
        "pronunciation": word_info[0].get("phonetic", "No pronunciation available"),
        "synonyms": word_info[0]
        .get("meanings", [{}])[0]
        .get("synonyms", []),
        "example": word_info[0]
        .get("meanings", [{}])[0]
        .get("definitions", [{}])[0]
        .get("example", "No example available"),
    }

    return word_details
