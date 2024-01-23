
from __future__ import annotations

from sqlalchemy.orm import Session

from .wrapper import session_wrapper
from ..objects import Penguin

@session_wrapper
def fetch_by_id(id: int, session: Session | None = None):
    return session.query(Penguin) \
        .filter(Penguin.id == id) \
        .first()

@session_wrapper
def fetch_by_name(name: str, session: Session | None = None):
    return session.query(Penguin) \
        .filter(Penguin.username == name) \
        .first()

@session_wrapper
def fetch_by_nickname(nickname: str, session: Session | None = None):
    return session.query(Penguin) \
        .filter(Penguin.nickname == nickname) \
        .first()
