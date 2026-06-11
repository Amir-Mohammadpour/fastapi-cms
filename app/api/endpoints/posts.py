from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_post
from app.database import get_db
from app.schemas.post import Post, PostCreate, PostUpdate
from app.models.user import User
from ..deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[Post])
async def read_posts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud_post.get_posts(db, skip=skip, limit=limit)


@router.get("/{post_id}/", response_model=Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = await crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_post.create_post(db=db, post=post, user_id=current_user.id)


@router.put("/{post_id}/", response_model=Post)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_post = await crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post.",
        )
    updated_post = await crud_post.update_post(
        db=db, post_id=post_id, post_update=post_update
    )
    if updated_post is None:
        raise HTTPException(status_code=500, detail="Failed to update post")
    return updated_post


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_post = await crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post.",
        )
    await crud_post.delete_post(db=db, post_id=post_id)
