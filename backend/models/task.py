#!/usr/bin/python3
""" holds class Task"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Task(BaseModel, Base):
    """Representation of a Task """
    if storage_t == 'db':
        __tablename__ = 'tasks'
        project_id = Column(String(128), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(Text, nullable=False)
        instruction = Column(Text, nullable=False)
        points = Column(Integer, default=0)
        code_output = Column(Text, nullable=False)
        type = Column(String(128), nullable=False)
        order_index = Column(String(128), nullable=False)
        difficulty = Column(String(128), nullable=False)
        language = Column(String(128), nullable=False)
        image_url = Column(String(255), nullable=True)
        test_cases = relationship("TestCase", backref="tasks", cascade='all, delete')
        submissions = relationship("Submission", backref="tasks", cascade='all, delete')
    else:
        project_id = ""
        name = ""
        description = ""
        instruction = ""
        points = ""
        code_output = ""
        order_index = ""
        type = ""
        difficulty = ""
        language = ""
        image_url = ""

    def __init__(self, *args, **kwargs):
        """initializes task"""
        super().__init__(*args, **kwargs)