# 🐳 Docker & Kubernetes 실전 가이드

Docker와 Kubernetes를 실습하며 정리하는 학습 저장소입니다.

## 📦 Docker Compose 실습

**PostgreSQL + FastAPI + React**로 구성된 Todo CRUD 앱

| 서비스 | 스택 | 설명 |
|--------|------|------|
| `postgresdb` | PostgreSQL 16 | 데이터 저장소 (named volume) |
| `backend` | FastAPI | REST API 서버 |
| `frontend` | React(Vite) + nginx | UI, `/api` 요청은 backend 로 프록시 |

```
.
├── backend/             FastAPI API 서버
├── frontend/            React 앱 + nginx
├── docker-compose.yml   3개 컨테이너 정의
└── docs/                학습 문서
```

## 🚀 실행

```bash
docker compose up --build   # http://localhost:3000
docker compose down         # 종료 (-v : DB 볼륨까지 삭제)
```
