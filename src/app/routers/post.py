from datetime import datetime
from enum import Enum

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, models
from fastapi import Depends, HTTPException, status, APIRouter
from src.database import get_async_session
from ...auth.manager import fastapi_users
from ...auth.models import User

router = APIRouter()
current_user = fastapi_users.current_user()


class SortBy(str, Enum):
    id = "id"
    title = "title"
    date = "created_at"
    like = "likes_count"


class CounterChoice(str, Enum):
    like = "likes_count"
    comment = "comments_count"


def convertToPydanticSchema(posts):
    dictPosts = []
    for post in posts:
        temp = {"id": post.id, "user_id": post.user_id, "title": post.title, "content": post.content, "image": post.image, "created_at": post.created_at, "updated_at": post.updated_at, "likes_count": post.likes_count, "categories": [], "username": ""}
        dictPosts.append(temp)
    return dictPosts

# список постов с пагинатором
@router.get('/', response_model=schemas.ListPostResponse)
async def get_posts(db: AsyncSession = Depends(get_async_session), limit: int = 10,
                    page: int = 1, sortby: SortBy = SortBy.id):
    skip = (page - 1) * limit
    # posts = db.query(models.Post).group_by(models.Post.id).limit(limit).offset(skip).all()
    # posts = await db.execute(select(models.Post).group_by(models.Post.id).limit(limit).offset(skip))
    posts = await db.execute(select(models.Post).order_by(getattr(models.Post, sortby).desc()).limit(limit).offset(skip))
    posts = posts.scalars().all()
    dictPosts = convertToPydanticSchema(posts)
    for post in dictPosts:
        cids = await db.execute(select(models.PostCategories).where(models.PostCategories.post_id == post["id"]))
        cids = cids.scalars().all()
        for cid in cids:
            category = await db.execute(select(models.Category).where(models.Category.id == cid.category_id))
            category = category.scalars().all()[0]
            post["categories"].append(category)
        username = await db.execute(select(models.User).where(models.User.id == post["user_id"]))
        post["username"] = username.scalars().all()[0].username
    return {'status': 'success', 'results': len(dictPosts), 'posts': dictPosts}

# Поиск по постам
@router.get('/search', response_model=schemas.ListPostResponse)
async def get_posts(db: AsyncSession = Depends(get_async_session), query: str = "", limit: int = 10,
                    page: int = 1, sortby: SortBy = SortBy.id):
    if query == None or len(query) == 0:
        raise HTTPException(status_code=status. HTTP_400_BAD_REQUEST,
                            detail=f"Пустой запрос поиска")
    skip = (page - 1) * limit
    # posts = db.query(models.Post).group_by(models.Post.id).limit(limit).offset(skip).all()
    # posts = await db.execute(select(models.Post).group_by(models.Post.id).limit(limit).offset(skip))
    temp = await db.execute(select(models.Post).filter(models.Post.title.like("%" + query + "%")).order_by(getattr(
        models.Post, sortby).desc()).limit(limit).offset(skip))
    temp2 = await db.execute(select(models.Post).filter(models.Post.content.like("%" + query + "%")).order_by(getattr(
        models.Post, sortby).desc()).limit(limit).offset(skip))
    temp = temp.scalars().all()
    temp2 = temp2.scalars().all()
    posts = [*temp,*temp2]
    dictPosts = convertToPydanticSchema(posts)
    for post in dictPosts:
        cids = await db.execute(select(models.PostCategories).where(models.PostCategories.post_id == post["id"]))
        cids = cids.scalars().all()
        for cid in cids:
            category = await db.execute(select(models.Category).where(models.Category.id == cid.category_id))
            category = category.scalars().all()[0]
            post["categories"].append(category)
        username = await db.execute(select(models.User).where(models.User.id == post["user_id"]))
        post["username"] = username.scalars().all()[0].username
    return {'status': 'success', 'results': len(dictPosts), 'posts': dictPosts}


# получить один пост по id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
async def get_post(id: str, db: AsyncSession = Depends(get_async_session)):
    # post = await db.query(models.Post).filter(models.Post.id == id).first()
    q = await db.execute(select(models.Post).filter(models.Post.id == id))
    post = q.scalar()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Пост с id: {id} не найден")
    return post


# начислить +1 лайк или +1 коммент на пост (вычитание пока не требуется)
# @router.put('/counter/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.UpdatePostSchema)
@router.put('/{id}/counter', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
async def update_counter_post(counter: CounterChoice, id: str, db: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)):
    q = await db.execute(select(models.Post).filter(models.Post.id == id, models.Post.user_id == user.id))
    post_query = q.scalar()

    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Пост с id: {id} не найден")

    setattr(post_query, counter, getattr(post_query, counter) + 1)

    await db.commit()
    return post_query


# обновить пост
@router.put('/{id}', response_model=schemas.PostResponse)
async def update_post(id: str, post: schemas.UpdatePostSchema, db: AsyncSession = Depends(get_async_session)
                      , user: User = Depends(current_user)
                      ):
    # post_query = db.query(models.Post).filter(models.Post.id == id)
    post_query = await db.execute(select(models.Post).filter(models.Post.id == id))
    updated_post = post_query.scalar()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"Пост с id: {id} не найден")
    if updated_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='У вас нет доступа к данному действию')
    post.user_id = 1
    post.updated_at = datetime.now().timestamp()

    q = update(models.Post).where(models.Post.id == id).values(post.dict(exclude_unset=True))

    q = await db.execute(q)
    # updated_post = q.scalar()

    # post_query.update(post.dict(exclude_unset=True), synchronize_session=False)
    await db.commit()
    return updated_post


# создать пост
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.CreatePostSchema, db: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    post.user_id = user.id
    post.created_at = datetime.now().timestamp()
    post.updated_at = datetime.now().timestamp()
    post.likes_count = 0
    post.comments_count = 0
    new_post = models.Post(**post.dict())

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

