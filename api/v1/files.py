import os

from http import HTTPStatus
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.handlers import post_new_file
from api.v1.models import AddFile
from db.connectors import get_db_session, get_current_user_uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/wav", "audio/x-wav",
    "audio/ogg",
    "audio/flac",
    "audio/x-flac"
}

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac"}

@router.post("/upload", response_model=AddFile)
async def add_file(file_name: str = Form(...),
    file: UploadFile = File(...),
    user_uuid: UUID = Depends(get_current_user_uuid),
    session: AsyncSession = Depends(get_db_session)
):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unknown file type. Only audiofiles allowed"
        )

    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown file extension {file_ext}"
        )

    try:
        file_ext = os.path.splitext(file.filename)[1]
        saved_filename = f"{uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, saved_filename)

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        file_data = AddFile(filename=file_name, path=file_path, user_id=user_uuid)
        success = await post_new_file(session, file=file_data)

        if not success:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to save file metadata"
            )

        return file_data

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}"
        )
