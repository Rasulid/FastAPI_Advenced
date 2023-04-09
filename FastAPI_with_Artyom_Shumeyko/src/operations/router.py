import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List
from database import get_async_session
from operations.model import operation
from operations.schemas import OperationCreate

router = APIRouter(tags=['Operations'],
                   prefix='/operations')


@router.get('long_operation')
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


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    result = await session.execute(stmt)
    await session.commit()

    return {"status": "success"}
