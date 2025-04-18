from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False
    
class TodoCreate(BaseModel):
    title: str

todos: List[Todo] = []

@app.get("/")
async def root():
    return {"message": "Todo API"}

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return todos
    
@app.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    new_id = todos[-1].id + 1 if todos else 1
    new_todo = Todo(id=new_id, title=todo.title)
    todos.append(new_todo)
    return new_todo