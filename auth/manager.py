import httpx

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse


from sqlalchemy.ext.asyncio import AsyncSession

from settings import yandex

from api.v1.handlers import get_user_by_email, post_new_user
from api.v1.models import CreateUser
from db.connectors import get_db_session


router = APIRouter()

YANDEX_CLIENT_ID = yandex.client_id
YANDEX_CLIENT_SECRET = yandex.client_secret
YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"

@router.get("/login/yandex")
async def login_yandex():
    return RedirectResponse(
        f"{YANDEX_AUTH_URL}?response_type=code&client_id={YANDEX_CLIENT_ID}"
    )


@router.get("/auth/yandex/callback")
async def auth_callback(request: Request, code: str = None, session: AsyncSession = Depends(get_db_session)):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": YANDEX_CLIENT_ID,
                "client_secret": YANDEX_CLIENT_SECRET
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid code")

        access_token = token_response.json()["access_token"]

        user_response = await client.get(
            YANDEX_USER_INFO_URL,
            params={"format": "json"},
            headers={"Authorization": f"OAuth {access_token}"}
        )

        user_data = user_response.json()

        user = await get_user_by_email(session, user_data["emails"][0])
        if not user:
            user = CreateUser(name=user_data["login"], email=user_data["emails"][0])
            await post_new_user(session, user=user)

        if not user.is_active:
            raise HTTPException(status_code=403, detail="User is not active")

        request.session["user_uuid"] = str(user.id)
        request.session["is_superuser"] = user.is_superuser

        return RedirectResponse(url="/pages/index")


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/pages/index", status_code=303)
