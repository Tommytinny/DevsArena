#!/usr/bin/python3
""" holds class test result"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text, Boolean


class TestResult(BaseModel, Base):
    """Representation of a testresult """
    if storage_t == 'db':
        __tablename__ = 'test_results'
        submission_id = Column(String(128), ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
        task_id = Column(String(128), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
        test_case_id = Column(String(128), ForeignKey('test_cases.id', ondelete='CASCADE'), nullable=False)
        name = Column(String(128), nullable=False)
        status = Column(String(128), nullable=False)
        actual_output = Column(Text, nullable=True)
        passed = Column(Boolean, default=False)
    else:
        name = ""
        status = ""
        actual_output = ""
        passed = ""

    def __init__(self, *args, **kwargs):
        """initializes test_result"""
        super().__init__(*args, **kwargs)