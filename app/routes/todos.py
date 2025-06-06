from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, Todo as TodoSchema
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=TodoSchema)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_todo = Todo(**todo.dict(), owner_id=current_user["id"])
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
