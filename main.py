from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional

DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False

class TodoCreate(SQLModel):
    title: str

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def root():
    return {"message": "Todo API"}

@app.get("/todos", response_model=List[Todo])
def get_todos(session: Session = Depends(get_session)):
    return session.exec(select(Todo)).all()
    
@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    new_todo = Todo(title=todo.title)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo
    
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return
    
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo