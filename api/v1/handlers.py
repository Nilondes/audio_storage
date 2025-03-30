from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, insert

from api.v1.models import CreateUser, AddFile
from db.models import User, File


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    """Select all users."""

    stmt = select(User)
    result = await session.execute(stmt)

    return result.scalars().all()


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    """Select user by email."""

    stmt = select(User).where(User.email == email)
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


async def post_new_file(session: AsyncSession, file: AddFile) -> bool:
    """Add new file."""

    stmt = insert(File).values(file.dict())
    result = await session.execute(stmt)
    await session.commit()

    if result:
        return True

    return False
