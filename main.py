import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).parent
SEED_FILE = BASE_DIR / "seed" / "items.json"  # 1. 이미지: 빌드 시 고정
NOTES_FILE = BASE_DIR / "tmp" / "notes.txt"  # 2. 임시: 컨테이너 read-write 레이어
USERS_FILE = BASE_DIR / "data" / "users.json"  # 3. 영구: 볼륨을 마운트하는 위치

app = FastAPI(title="Dummy Backend")


class Item(BaseModel):
    id: int
    name: str
    price: float


class NoteIn(BaseModel):
    text: str = Field(min_length=1, max_length=200)


class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class User(UserIn):
    id: int


def load_items() -> list[Item]:
    return [Item(**raw) for raw in json.loads(SEED_FILE.read_text())]


def load_users() -> list[User]:
    if not USERS_FILE.exists():
        return []
    return [User(**raw) for raw in json.loads(USERS_FILE.read_text())]


@app.get("/health")
def health():
    return {"status": "ok"}


# --- 1. 이미지 데이터: 읽기 전용 seed ---
@app.get("/items")
def list_items() -> list[Item]:
    return load_items()


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    for item in load_items():
        if item.id == item_id:
            return item
    raise HTTPException(404, "item not found")


# --- 2. 임시 데이터: 컨테이너 제거 시 사라짐 ---
@app.post("/notes", status_code=201)
def add_note(note: NoteIn) -> dict[str, str]:
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NOTES_FILE.open("a") as f:
        f.write(note.text.replace("\n", " ") + "\n")
    return {"text": note.text}


@app.get("/notes")
def list_notes() -> list[str]:
    if not NOTES_FILE.exists():
        return []
    return NOTES_FILE.read_text().splitlines()


# --- 3. 영구 데이터: 볼륨에 저장 ---
@app.post("/users", status_code=201)
def add_user(user: UserIn) -> User:
    users = load_users()
    created = User(id=len(users) + 1, name=user.name)
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps([u.model_dump() for u in [*users, created]]))
    return created


@app.get("/users")
def list_users() -> list[User]:
    return load_users()
