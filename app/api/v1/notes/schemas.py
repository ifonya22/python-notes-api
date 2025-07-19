from typing import Optional

from pydantic import BaseModel, Field

from app.config import settings
from app.utils.fields import PyObjectId


class CreateNoteRequestV1(BaseModel):
    title: str = Field(..., max_length=settings.note_rules.title_max_lenght)
    body: str = Field(..., max_length=settings.note_rules.body_max_lenght)


class UpdateNoteRequestV1(BaseModel):
    title: Optional[str] = Field(default=None, max_length=settings.note_rules.title_max_lenght)
    body: Optional[str] = Field(default=None, max_length=settings.note_rules.body_max_lenght)


class NoteResponseV1(BaseModel):
    note_id: PyObjectId = Field(..., alias="_id")
    title: str
    body: str


class NoteResponseAdminV1(NoteResponseV1):
    user_id: int
    is_deleted: bool
