import uvicorn
from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_users import FastAPIUsers
from app.auth.models import User
from app.auth.manager import get_user_manager
from app.auth.methods import auth_backend
from app.auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware
from app.pages.router import app as router_pages
from pydantic import BaseModel
from typing import List
from redis import asyncio as aioredis

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_pages)

current_user = fastapi_users.current_user()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Проверка, аутентифицирован ли пользователь, если нет то выдаст ошибку 401
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


dict_users = [{"ID": 100059, "STATUS_ID": "F", "status": "completed", "shop_ID": "1021440"},
              {"ID": 100060, "STATUS_ID": "F", "status": "completed", "shop_ID": "1021576"},
              {"ID": 100061, "STATUS_ID": "F", "status": "canceled", "shop_ID": "1021841"}]


class Valid(BaseModel):
    ID: int
    STATUS_ID: str
    status: str
    shop_ID: str


@app.get('/valid/{user_id}', response_model=List[Valid])
def valid_true(user_id: int):
    return [user for user in dict_users if user.get('ID') == user_id]


# это функция позволяет нам воспользоваться декоратором @cache
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# сохраняем данные в виде ключ-значение в кэширование 
@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world")


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0', reload=False, workers=None)