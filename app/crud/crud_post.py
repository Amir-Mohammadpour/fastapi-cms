from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.post import Post
from ..schemas.post import PostCreate, PostUpdate


async def get_post(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(select(Post).filter(Post.id == post_id))
    return result.scalar_one_or_none()


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Post]:
    result = await db.execute(select(Post).offset(skip).limit(limit))
    return result.scalars().all()


async def create_post(db: AsyncSession, post: PostCreate, user_id: int) -> Post:
    db_post = Post(**post.model_dump(), author_id=user_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def update_post(
    db: AsyncSession, post_id: int, post_update: PostUpdate
) -> Post | None:
    db_post = await get_post(db, post_id)
    if not db_post:
        return None

    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, post_id: int) -> Post | None:
    db_post = await get_post(db, post_id)
    if not db_post:
        return None
    await db.delete(db_post)
    await db.commit()
    return db_post
