#!/usr/bin/python3
""" holds class grade"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Grade(BaseModel, Base):
    """Representation of a grade """
    if storage_t == 'db':
        __tablename__ = 'grades'
        student_id = Column(String(128), ForeignKey('users.id'), nullable=False)
        course_id = Column(String(128), ForeignKey('courses.id'), nullable=False)
        practical_score = Column(Integer, nullable=True)
        exam_score = Column(Integer, nullable=True)
        total_score = Column(Integer, nullable=True)
        grade = Column(String(50), nullable=True)
    else:
        student_id = ""
        course_id = ""
        practical_score = ""
        exam_score = ""
        total_score = ""
        grade = ""
        

    def __init__(self, *args, **kwargs):
        """initializes grade"""
        super().__init__(*args, **kwargs)