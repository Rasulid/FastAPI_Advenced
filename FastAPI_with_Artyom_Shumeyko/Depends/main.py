from fastapi import FastAPI, Depends, HTTPException
from starlette.requests import Request

app = FastAPI()


# Depends with "yield"
async def get_async_session():
    print("Получения Сессии")
    session = "Session"
    yield session
    print("Уничтожения Сессии")


@app.get("/yields")
async def read_root(session=Depends(get_async_session)):
    print(session)
    return {"message": "Hello World"}


# parametrs

def params(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}


@app.get("/parameters")
async def read_root(parametr: dict = Depends(params)):
    return parametr


# Class

class Parametrs:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip


@app.get("/class")
async def read_root(parametr: Parametrs = Depends(Parametrs)):
    return parametr


# auth

class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        if "super_cookie" not in request.cookies:
            raise HTTPException(status_code=403, detail="Запрешено")
        return True


auth_geuard_payment = AuthGuard("peymed_payment")


@app.get("/auth", dependencies=[Depends(auth_geuard_payment)])
async def read_root():
    return "True"
