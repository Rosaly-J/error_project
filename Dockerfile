FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --no-cache-dir poetry

# Poetry 설정 (가상 환경 비활성화)
RUN poetry config virtualenvs.create false

# pyproject.toml 및 poetry.lock 파일 복사
COPY pyproject.toml poetry.lock ./

# 의존성 설치
RUN poetry install --no-dev --no-interaction --no-ansi

# 애플리케이션 소스 복사
COPY . .

# FastAPI 실행 (uvicorn 사용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]