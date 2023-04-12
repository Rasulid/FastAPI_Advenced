from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks

from auth.base_config import current_user
from tasks.tasks import send_email_v2

router = APIRouter(prefix="/report")


# @router.get('/msg')
# async def get_msg(user=Depends(current_user)):
#     send_email.delay(user.email)
#     return {"status": 200,
#             'data': "sent",
#             'details': None}
#

@router.get('/msg/v2')
async def get_msg_v2(user=Depends(current_user)):
    send_email_v2.delay(user.email)
    return {"status": 200,
            'data': "sent",
            'details': None}
