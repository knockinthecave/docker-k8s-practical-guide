import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel

DATABASE_URL = os.environ["DATABASE_URL"]


def query(sql, params=()):
    # ponytail: 요청마다 새 연결, 트래픽이 늘면 커넥션 풀(psycopg_pool)로 교체
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        cur = conn.execute(sql, params)
        return cur.fetchall() if cur.description else []


@asynccontextmanager
async def lifespan(_: FastAPI):
    query(
        "CREATE TABLE IF NOT EXISTS todos ("
        "id SERIAL PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT FALSE)"
    )
    yield


app = FastAPI(lifespan=lifespan)


class TodoIn(BaseModel):
    title: str
    done: bool = False


@app.get("/todos")
def list_todos():
    return query("SELECT * FROM todos ORDER BY id")


@app.post("/todos", status_code=201)
def create_todo(todo: TodoIn):
    return query(
        "INSERT INTO todos (title, done) VALUES (%s, %s) RETURNING *",
        (todo.title, todo.done),
    )[0]


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoIn):
    rows = query(
        "UPDATE todos SET title = %s, done = %s WHERE id = %s RETURNING *",
        (todo.title, todo.done, todo_id),
    )
    if not rows:
        raise HTTPException(404, "todo not found")
    return rows[0]


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if not query("DELETE FROM todos WHERE id = %s RETURNING id", (todo_id,)):
        raise HTTPException(404, "todo not found")
