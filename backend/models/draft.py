#!/usr/bin/python3
"""Draft model to persist inline editor content for tasks."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text


class Draft(BaseModel, Base):
    """Representation of a Draft for storing editor content"""
    try:
        from models import storage_t
    except Exception:
        storage_t = 'db'

    if storage_t == 'db':
        __tablename__ = 'drafts'
        user_id = Column(String(128), nullable=False)
        task_id = Column(String(128), nullable=False)
        code = Column(Text, nullable=True)
        language = Column(String(64), nullable=True)
    else:
        user_id = ""
        task_id = ""
        code = ""
        language = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
