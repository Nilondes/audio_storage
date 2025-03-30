from uuid import UUID

from fastapi import Request, HTTPException, Depends
from sqlalchemy import Boolean

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import settings as SETTINGS

from db.models import User

connection_string = (f"postgresql+asyncpg://{SETTINGS.user}"
                     f":{SETTINGS.password.get_secret_value()}"
                     f"@{SETTINGS.host}:{SETTINGS.port}/{SETTINGS.database}")

engine = create_async_engine(connection_string, future=True, echo=True)
pg_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    try:
        session: AsyncSession = pg_session()
        yield session
    finally:
        await session.close()


async def get_current_user_uuid(
        request: Request
) -> UUID:
    user_uuid = request.session.get("user_uuid")
    if not user_uuid:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return UUID(user_uuid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user UUID")
