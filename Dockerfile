FROM python:3.14.5-alpine

# 베이스 이미지에 포함된 OS 패키지의 보안 패치 적용
RUN apk upgrade --no-cache

WORKDIR /app

# 의존성을 먼저 복사해 레이어 캐시 활용 (코드만 바뀌면 pip install 생략)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]