from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.handlers import get_all_users, get_user_by_email, post_new_user
from api.v1.models import CreateUser, User
from db.connectors import get_db_session

router = APIRouter()

@router.get("/users", response_model=List[User])
async def get_users(session: AsyncSession = Depends(get_db_session)):
    users = await get_all_users(session)

    if not users:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No users found")

    return users


@router.get("/users/{email}", response_model=User)
async def get_user(email: str,
                   session: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_email(session, email=email)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No user found")

    return user


@router.post("/users", response_model=User)
async def add_user(user: CreateUser,
                   session: AsyncSession = Depends(get_db_session)):
    success = await post_new_user(session, user=user)

    if not success:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="No user created")

    return user


@router.delete("/users/{email}", response_model=User)
async def del_user():
    return None
