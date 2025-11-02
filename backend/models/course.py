#!/usr/bin/python3
""" holds class Course"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Course(BaseModel, Base):
    """Representation of a Course """
    if storage_t == 'db':
        __tablename__ = 'courses'
        instructor_id = Column(String(128), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
        title = Column(String(255), nullable=False)
        course_code = Column(String(50), nullable=False)
        level_id = Column(String(128), ForeignKey('levels.id', ondelete='CASCADE'), nullable=False)
        units = Column(Integer, nullable=False)
        description = Column(Text, nullable=False)
        projects = relationship("Project", backref="courses", cascade='all, delete')
        grades = relationship("Grade", backref="courses")
    else:
        instructor_id = ""
        title = ""
        course_code = ""
        level_id = ""
        units = ""
        description = ""

    def __init__(self, *args, **kwargs):
        """initializes course"""
        super().__init__(*args, **kwargs)