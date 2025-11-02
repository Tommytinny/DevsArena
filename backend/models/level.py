#!/usr/bin/python3
""" holds class Level"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship



class Level(BaseModel, Base):
    """Representation of a level """
    if storage_t == 'db':
        __tablename__ = 'levels'
        name = Column(String(128), nullable=False)
        academic_year = Column(String(128), nullable=False)
        semester = Column(String(128), nullable=False)
        course = relationship("Course", backref="levels")
        students = relationship("User", back_populates="level")
        
        
        #task_result = relationship("TaskResult", backref="users")
    else:
        name = ""
        academic_year = ""
        semester = ""

    def __init__(self, *args, **kwargs):
        """initializes level"""
        super().__init__(*args, **kwargs)
