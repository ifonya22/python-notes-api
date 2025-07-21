from pydantic import BaseModel, Field


class Note(BaseModel):
    title: str = Field(..., max_length=256)
    body: str = Field(..., max_length=65536)
