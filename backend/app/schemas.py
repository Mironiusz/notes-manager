from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel
from pydantic import ConfigDict, constr

from .models import to_camel

class NoteCreate(SQLModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
    title: constr(strip_whitespace=True, min_length=1)
    content: str = ""
    is_favourite: bool = False

class NoteUpdate(SQLModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
    title: Optional[constr(strip_whitespace=True, min_length=1)] = None
    content: Optional[str] = None
    is_favourite: Optional[bool] = None
