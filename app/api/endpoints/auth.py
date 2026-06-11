from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core.security import create_access_token, verify_password
from app.crud import crud_user
from app.database import get_db
from app.schemas.user import User, UserCreate
from app.schemas.token import Token
from app.core.config import settings

router = APIRouter()


@router.post("/register/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_registration(
    user_in: UserCreate, db: AsyncSession = Depends(get_db)
):
    user = await crud_user.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return await crud_user.create_user(db=db, user=user_in)


@router.post("/login/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await crud_user.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},  # ← باید string باشه
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
