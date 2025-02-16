from pydantic import BaseModel
from sqlalchemy import select, insert, literal, literal_column

from src.database import engine


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


    async def add(self, data):
        add_statement = insert(self.model).values(**data.model_dump()).returning(literal_column('*'))
        result = await self.session.execute(add_statement)
        return result.one()