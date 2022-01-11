from typing import List

from pydantic import BaseModel


class Todo(BaseModel):
    content: str

    class Config:
        orm_mode = True


class TodoOut(BaseModel):
    todos: List[Todo]


class TodoStatus(BaseModel):
    todo: Todo
    status: str


class TodoAdded(TodoStatus):
    status = "added"


class TodoDeleted(TodoStatus):
    status = "deleted"
