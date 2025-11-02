#!/usr/bin/python3
""" holds class Event"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey


class Timetable(BaseModel, Base):
    """Representation of a Timetable """
    if storage_t == 'db':
        __tablename__ = 'timetables'
        level_id = Column(String(128), ForeignKey('levels.id'), nullable=False)
        course_name = Column(String(255), nullable=False)
        day = Column(Integer, nullable=False)
        start_time = Column(Integer, nullable=False)
        duration = Column(Integer, nullable=False)
    else:
        course_name = ""
        day = ""
        start_time = ""
        duration = ""

    def __init__(self, *args, **kwargs):
        """initializes timetable"""
        super().__init__(*args, **kwargs)