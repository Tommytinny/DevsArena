#!/usr/bin/python3
""" holds class Submission"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship


class TestCase(BaseModel, Base):
    """Representation of a submission """
    if storage_t == 'db':
        __tablename__ = 'test_cases'
        task_id = Column(String(128), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
        name = Column(String(255), nullable=False)
        input = Column(Text, nullable=False)
        expected = Column(Text, nullable=False)
        points = Column(Integer, default=0)
        order_index = Column(String(50), nullable=False)
        test_result = relationship("TestResult", backref="test_cases", cascade='all, delete')
    else:
        name = ""
        input = ""
        expected = ""
        points = ""

    def __init__(self, *args, **kwargs):
        """initializes task_case"""
        super().__init__(*args, **kwargs)