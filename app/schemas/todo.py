from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str | None = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    title: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True
        