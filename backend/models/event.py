#!/usr/bin/python3
""" holds class Event"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey


class Event(BaseModel, Base):
    """Representation of a Event """
    if storage_t == 'db':
        __tablename__ = 'events'
        level_id = Column(String(128), ForeignKey('levels.id'), nullable=False)
        title = Column(String(255), nullable=False)
        date = Column(DateTime, nullable=False)
        venue = Column(String(255), nullable=True)
        type = Column(String(50), nullable=False)
    else:
        title = ""
        date = ""
        venue = ""
        type = ""

    def __init__(self, *args, **kwargs):
        """initializes event"""
        super().__init__(*args, **kwargs)