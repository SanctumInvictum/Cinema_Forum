from sqlalchemy import select, update

from starlette import status
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request, HTTPException

from src.app import models
from src.database import get_async_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/', name='index')
def get_posts(db: Session = Depends(get_async_session), request: Request = None):
    return templates.TemplateResponse("index.html",  {"request": request})


@router.get('/reviews/{id}', name='review')
async def get_posts(id: str, db: Session = Depends(get_async_session), request: Request = None):
    q = await db.execute(select(models.Post).filter(models.Post.id == id))
    post = q.scalar()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Пост с id: {id} не найден")

    print(post.__table__.columns)

    return templates.TemplateResponse("review.html",  {"request": request, "post": post})


@router.get('/popular', name='popular_reviews')
def get_posts(db: Session = Depends(get_async_session), request: Request = None):
    return templates.TemplateResponse("popular_reviews.html",  {"request": request})


@router.get('/texteditor', name='text_editor')
def get_posts(db: Session = Depends(get_async_session), request: Request = None):
    return templates.TemplateResponse("text_editor.html",  {"request": request})


@router.get('/signup', name='signup')
def get_posts(db: Session = Depends(get_async_session), request: Request = None):
    return templates.TemplateResponse("signup.html",  {"request": request})

@router.get('/search', name='search')
def get_posts(db: Session = Depends(get_async_session), request: Request = None):
    return templates.TemplateResponse("search.html",  {"request": request})