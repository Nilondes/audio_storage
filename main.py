import uvicorn
from fastapi import FastAPI

from auth.manager import router as yandex_router
from api.v1.users import router as users_router


app = FastAPI()


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
