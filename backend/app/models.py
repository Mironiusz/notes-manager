from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

def to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])

class Note(SQLModel, table=True):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str = ""
    is_favourite: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
