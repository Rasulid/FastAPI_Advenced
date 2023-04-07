from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.model import operation
from operations.schemas import OperationCreate

router = APIRouter(tags=['Operations'],
                   prefix='/operations')


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    print(result)
    return result.scalars().all()


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    result = await session.execute(stmt)
    await session.commit()
    return {"status": "success"}