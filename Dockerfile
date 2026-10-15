FROM python:3.14.5-alpine

# 베이스 이미지에 포함된 OS 패키지의 보안 패치 적용
RUN apk upgrade --no-cache

WORKDIR /app

# 의존성을 먼저 복사해 레이어 캐시 활용 (코드만 바뀌면 pip install 생략)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY seed/ ./seed/

# 임시 데이터(tmp), 영구 데이터(data, 볼륨 마운트 위치) 디렉토리
RUN mkdir -p /app/tmp /app/data

# ARG: 빌드 시점에만 존재 (--build-arg DEFAULT_PORT=9000)
ARG DEFAULT_PORT=8000

# ENV: 이미지·컨테이너 런타임까지 유지 (docker run -e PORT=9000 으로 덮어쓰기)
ENV PORT=$DEFAULT_PORT
ENV APP_NAME="docker-practice-app"

EXPOSE $PORT

# 환경변수 치환이 필요하므로 sh -c 사용 (exec로 uvicorn이 PID 1 유지)
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]