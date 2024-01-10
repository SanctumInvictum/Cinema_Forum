from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from starlette.staticfiles import StaticFiles

from src.config import settings
from src.auth.manager import get_user_manager, auth_backend, fastapi_users
from src.database import engine

from src.app.routers import post, home
from src.app.models import *
# from src.auth.models import *
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(title="Cinemaforum")

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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

app.include_router(post.router, tags=['Posts'], prefix='/api/posts')
app.include_router(home.router, tags=['Home'], prefix='/home')

app.mount("/static", StaticFiles(directory="static"), name="static")