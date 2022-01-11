from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from schemas import Todo, TodoOut
from core.exception import TodoIsNot, TodoisHave
from database.models import Todo as TodoModel


async def with_todo(db):
    return (await (db.execute(select(TodoModel)))).scalars()


async def create_todo_sync(todo: Todo, db) -> List[Todo]:
    try:
        async with db.begin_nested():
            db.execute(db.add(TodoModel(content=todo.content)))
    except IntegrityError:
        raise TodoisHave()

    return todo


async def delete_todo_sync(todo: Todo, db):
    async with db.begin_nested():
        exist = (await (
                db.execute(select(count()).select_from(
                        select(TodoModel).where(TodoModel.content == todo.content)
                    )
                )
            )
        ).scalars().one() > 0
        if not exist:
            raise TodoIsNot()

        await db.execute(delete(TodoModel).where(TodoModel.content == todo.content))
    return todo
