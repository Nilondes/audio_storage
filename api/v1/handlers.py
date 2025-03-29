from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, insert

from api.v1.models import CreateUser
from db.models import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    """Select all users."""

    stmt = select(User)
    result = await session.execute(stmt)

    return result.scalars().all()


async def get_user_by_name(session: AsyncSession, name: str) -> User:
    """Select user by name."""

    stmt = select(User).where(User.name == name)
    result = await session.execute(stmt)

    return result.scalars().first()


async def post_new_user(session: AsyncSession, user: CreateUser) -> bool:
    """Create new user."""

    stmt = insert(User).values(user.dict())
    result = await session.execute(stmt)
    await session.commit()

    if result:
        return True

    return False
