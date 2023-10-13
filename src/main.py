from fastapi import FastAPI
from authorization.base import router as router_auth
from pages.router import router as router_pages
app = FastAPI(
    title="Cinema Forum!"
)

app.include_router(router_auth)
app.include_router(router_pages)

# Для запуска прописываем в треминал в папке src:
# uvicorn main:app --reload
# И переходим по этому адресу для получения удобного интерфейса работы с бэкендом
# http://127.0.0.1:8000/docs