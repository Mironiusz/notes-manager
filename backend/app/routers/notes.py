from __future__ import annotations
from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, col
from datetime import datetime, timezone

from ..db import get_session
from ..models import Note
from ..schemas import NoteCreate, NoteUpdate

router = APIRouter(prefix="/api/v1/notes", tags=["notes"])

SortType = Literal[
    "created_desc",
    "created_asc",
    "updated_desc",
    "updated_asc",
]

@router.get("", response_model=list[Note])
def list_notes(
    session: Session = Depends(get_session),
    query: Optional[str] = Query(default=None, description="fraza do wyszukiwania (tytuł)"),
    favourite: Optional[bool] = Query(default=None, description="true/false"),
    sort: SortType = "created_desc",
):
    stmt = select(Note)

    if query:
        q = f"%{query}%"
        stmt = stmt.where(col(Note.title).collate("NOCASE").like(q))

    if favourite is not None:
        stmt = stmt.where(Note.is_favourite == favourite)

    elif sort == "created_desc":
        stmt = stmt.order_by(Note.created_at.desc())
    elif sort == "created_asc":
        stmt = stmt.order_by(Note.created_at.asc())
    elif sort == "updated_asc":
        stmt = stmt.order_by(Note.updated_at.asc())
    else:
        stmt = stmt.order_by(Note.updated_at.desc())


    return session.exec(stmt).all()

@router.get("/{note_id}", response_model=Note)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    return note

@router.post("", response_model=Note, status_code=201)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)):
    note = Note.model_validate(payload.model_dump())
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.patch("/{note_id}", response_model=Note)
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(404, "Note not found")

    changed = False
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(note, k, v)
        changed = True
    if changed:
        note.updated_at = datetime.now(timezone.utc)

    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    session.delete(note)
    session.commit()
