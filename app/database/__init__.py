from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.factory import RepositoryDBFactory
from app.database.mongo.client import get_mongo_db
from app.database.sql.session import get_sql_session


async def get_repository_factory(
    sql_session: AsyncSession = Depends(get_sql_session),
    mongo_db=Depends(get_mongo_db),
):
    return RepositoryDBFactory(sql_session, mongo_db)
