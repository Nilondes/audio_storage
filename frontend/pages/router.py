from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from db.connectors import get_current_user_uuid


router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/index")
async def home(request: Request):
    try:
        await get_current_user_uuid(request)
    except:
        return RedirectResponse(
            url="/login/yandex",
            status_code=status.HTTP_302_FOUND
        )

    return templates.TemplateResponse(request, "index.html")
