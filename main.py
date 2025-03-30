import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from auth.manager import router as yandex_router
from api.v1.users import router as users_router
from api.v1.files import router as files_router
from frontend.pages.router import router as frontend_router



app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="secret_key",
    session_cookie="session_cookie",
    max_age=3600
)


app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["users"]
)


app.include_router(
    yandex_router,
    prefix="",
    tags=["auth"]
)


app.include_router(frontend_router)


app.include_router(
    files_router,
    prefix="/api/v1/files",
    tags=["files"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
