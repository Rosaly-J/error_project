import pytest
from fastapi.testclient import TestClient
from main import app

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

