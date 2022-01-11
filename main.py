from fastapi import FastAPI, Depends
from schemas import Todo, TodoAdded, TodoOut, TodoDeleted
from database.session import async_session, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.exception import TodoisHave, TodoIsNot
from database.crud import create_todo_sync, with_todo, delete_todo_sync

app = FastAPI()


@app.post("/todo")
async def todo(todo: Todo, db: AsyncSession = Depends(get_session)):
    try:
        await create_todo_sync(todo, db)
    except TodoisHave:
        return {"code": 404, "message": "todo is have"}
    return TodoAdded(todo=todo)


@app.get("/todo/")
async def get_todo(db: AsyncSession = Depends(get_session)):
    return TodoOut(
        todos=[Todo(content=todo.content) for todo in await with_todo(db)]
    )


@app.delete("/todo/")
async def delete_todo(todo: Todo, db: AsyncSession = Depends(get_session)):
    try:
        await delete_todo_sync(todo, db)
    except TodoIsNot:
        return {"code": 404, "message": "todo is note"}

    return {"code": 200, "mesage": "todo deleted"}
