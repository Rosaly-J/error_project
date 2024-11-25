import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime
from uuid import uuid4

client = TestClient(app)

# 가상의 사용자 ID와 검색 기록
fake_user_id = 1
fake_search_history = [
    {"search_id": uuid4(), "user_id": fake_user_id, "search_term": "apple", "search_date": datetime.now()},
    {"search_id": uuid4(), "user_id": fake_user_id, "search_term": "banana", "search_date": datetime.now()},
]
class TestWordSearch:
    client = TestClient(app)

    def test_search_word_valid(self):
        response = self.client.get("/search/word", params={"word": "example"})
        assert response.status_code == 200
        data = response.json()
        assert "word" in data
        assert "definitions" in data
        assert "pronunciation" in data
        assert "synonyms" in data
        assert "example" in data
        assert isinstance(data["definitions"], list)
        assert isinstance(data["synonyms"], list)

    def test_search_word_not_found(self):
        response = self.client.get("/search/word", params={"word": "nonexistentword"})
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Word not found"

    def test_search_word_missing_param(self):
        response = self.client.get("/search/word")
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert "loc" in data["detail"][0]
        assert data["detail"][0]["loc"] == ["query", "word"]


class TestSearchHistory:

    @pytest.fixture
    def setup_search_history(self):
        # 테스트 시작 전에 가상의 검색 기록을 데이터베이스에 삽입하는 코드가 여기에 들어갈 수 있습니다.
        # 예시로 이 데이터를 직접 사용하는 방식입니다.
        return fake_search_history

    def test_get_search_history(self, setup_search_history):
        # 검색 기록 조회 테스트
        response = client.get(f"/search/history?user_id={fake_user_id}&page=1&size=10")

        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert len(data["history"]) == 2  # 예시로 2개의 검색 기록이 반환되어야 함
        assert data["history"][0]["search_term"] == "apple"
        assert data["history"][1]["search_term"] == "banana"

    def test_delete_search_history(self, setup_search_history):
        # 특정 검색 기록 삭제 테스트
        search_id_to_delete = setup_search_history[0]["search_id"]
        response = client.delete(f"/search/history/{search_id_to_delete}?user_id={fake_user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Search record deleted successfully"

        # 삭제 후 기록 조회
        response = client.get(f"/search/history?user_id={fake_user_id}&page=1&size=10")
        data = response.json()
        assert len(data["history"]) == 1  # 하나의 기록만 남아 있어야 함
        assert data["history"][0]["search_term"] == "banana"

    def test_delete_all_search_history(self, setup_search_history):
        # 전체 검색 기록 삭제 테스트
        response = client.delete(f"/search/history/all?user_id={fake_user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "All search records deleted successfully"

        # 삭제 후 기록 조회
        response = client.get(f"/search/history?user_id={fake_user_id}&page=1&size=10")
        data = response.json()
        assert len(data["history"]) == 0  # 모든 기록이 삭제되어야 함