import pytest
from sqlalchemy import insert, select

from auth.model import role
from configtest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        print(result.all())
        """== [(1, 'admin', None)], Роль не добавилась"""

# def test_register():
#     assert 1 == 1
