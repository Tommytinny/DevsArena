#!/usr/bin/python3
""" holds class Submission"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship


class Submission(BaseModel, Base):
    """Representation of a submission """
    if storage_t == 'db':
        __tablename__ = 'submissions'
        student_id = Column(String(128), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
        task_id = Column(String(128), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
        project_id = Column(String(128), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
        file_url = Column(String(128), nullable=False)
        language = Column(String(128), nullable=False)
        status = Column(String(128))
        passed_tests = Column(Integer, nullable=True)
        score = Column(Integer)
        test_results = relationship("TestResult", backref="submissions", cascade='all, delete')
    else:
        student_id = ""
        task_id = ""
        project_id = ""
        code = ""
        language = ""
        status = ""
        passed_tests = ""
        score = ""
        

    def __init__(self, *args, **kwargs):
        """initializes submission"""
        super().__init__(*args, **kwargs)