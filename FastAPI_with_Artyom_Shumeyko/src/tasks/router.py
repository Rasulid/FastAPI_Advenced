from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks

from auth.base_config import current_user
from tasks.tasks import send_email

router = APIRouter(prefix="/report")

@router.get('/msg')
async def get_msg(background_tasks: BackgroundTasks,user= Depends(current_user)):
    background_tasks.add_task(send_email, user.username)
    return {"status": 200,
            'data': "sent",
            'details': None}