import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete, exc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List
from database import get_async_session
from operations.model import operation
from operations.schemas import OperationCreate
from auth.model import Learning, learning

router = APIRouter(tags=['Operations'],
                   prefix='/operations')


@router.get('/long_operation')
@cache(expire=30)
def long_operation():
    time.sleep(2)
    return "So many data"


@router.get("/", response_model=List[OperationCreate])
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        # return {'status': "success",
        #         "data": result.all(),
        #         "details": None}
        return result.all()
    except Exception:
        raise HTTPException(status_code=499, detail={
            'status': "error",
            "data": None,
            "details": None})


class Test_Schema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


@router.get('/test', response_model=List[Test_Schema])
async def learn(session: AsyncSession = Depends(get_async_session)):
    query = select(learning)
    result = await session.execute(query)
    return result.all()


@router.post('/test')
async def add_test_request(schema: Test_Schema, session: AsyncSession = Depends(get_async_session)):
    data = insert(learning).values(**schema.dict())
    result = await session.execute(data)
    await session.commit()
    return {"data": result}


@router.put('/test/{id}')
async def get_update(id: int, schema: Test_Schema, session: AsyncSession = Depends(get_async_session)):
    update_data = update(Learning).where(Learning.id == id).values(title=schema.title, description=schema.description)
    result = await session.execute(update_data)
    await session.commit()
    return {"data": result}


@router.delete("/test/{id}")
async def delete_test(id: int, session: AsyncSession = Depends(get_async_session)):
    test = await session.get(Learning, id)
    await session.delete(test)
    await session.commit()
    return {"message": f"Test with id {id} has been deleted."}


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    result = await session.execute(stmt)
    await session.commit()

    return {"status": "success"}
