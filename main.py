from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Dummy Backend")


class Item(BaseModel):
    id: int
    name: str
    price: float


ITEMS = [
    Item(id=1, name="keyboard", price=49.9),
    Item(id=2, name="mouse", price=19.9),
    Item(id=3, name="monitor", price=199.0),
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items() -> list[Item]:
    return ITEMS


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    for item in ITEMS:
        if item.id == item_id:
            return item
    raise HTTPException(404, "item not found")
