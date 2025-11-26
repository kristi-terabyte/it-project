"""
Persistence layer for SmartNotes CLI application.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "notes.json"


@dataclass(slots=True)
class Note:
    id: str
    title: str
    body: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds")
    )

    def matches_keyword(self, keyword: str) -> bool:
        pattern = keyword.lower()
        return (
            pattern in self.title.lower()
            or pattern in self.body.lower()
            or any(pattern in tag.lower() for tag in self.tags)
        )


class NoteStorage:
    """Lightweight JSON storage for notes."""

    def __init__(self, file_path: Path = DATA_FILE) -> None:
        self.file_path = file_path
        if not self.file_path.exists():
            self._write([])

    def _read(self) -> List[dict]:
        with self.file_path.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        return data

    def _write(self, notes: Iterable[dict]) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(list(notes), f, ensure_ascii=False, indent=2)

    def list_notes(self, tag: Optional[str] = None) -> List[Note]:
        items = [Note(**entry) for entry in self._read()]
        if tag:
            tag_lower = tag.lower()
            items = [note for note in items if tag_lower in (t.lower() for t in note.tags)]
        return items

    def add_note(self, title: str, body: str, tags: Optional[List[str]] = None) -> Note:
        tags = tags or []
        note = Note(id=str(uuid.uuid4()), title=title, body=body, tags=tags)
        notes = self._read()
        notes.append(note.__dict__)
        self._write(notes)
        return note

    def update_note(self, note_id: str, title: str, body: str, tags: Optional[List[str]] = None) -> Optional[Note]:
        tags = tags or []
        notes = self._read()
        updated: Optional[Note] = None
        for entry in notes:
            if entry["id"] == note_id:
                entry["title"] = title
                entry["body"] = body
                entry["tags"] = tags
                updated = Note(**entry)
                break
        if updated:
            self._write(notes)
        return updated

    def search(self, keyword: str) -> List[Note]:
        return [note for note in self.list_notes() if note.matches_keyword(keyword)]

    def delete(self, note_id: str) -> bool:
        notes = self._read()
        filtered = [entry for entry in notes if entry["id"] != note_id]
        if len(filtered) == len(notes):
            return False
        self._write(filtered)
        return True

