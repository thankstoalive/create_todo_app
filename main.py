from fastapi import FastAPI, HTTPException
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
    
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    for index, t in enumerate(todos):
        if t.id == todo_id:
            todos.pop(index)
            return
    raise HTTPException(status_code=404, detail="Todo not found")