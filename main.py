from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

todos: List[Todo] = []

@app.get("/")
async def root():
    return {"message": "Todo API"}

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return todos