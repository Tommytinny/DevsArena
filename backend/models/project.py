#!/usr/bin/python3
""" holds class Course"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship


class Project(BaseModel, Base):
    """Representation of a Project """
    if storage_t == 'db':
        __tablename__ = 'projects'
        course_id = Column(String(128), ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
        name = Column(String(255), nullable=False)
        description = Column(Text, nullable=False)
        start = Column(DateTime, nullable=False)
        deadline = Column(DateTime, nullable=False)
        total_points = Column(Float, default=0)
        #completed = Column(Boolean, default=False)
        project_type = Column(Text, nullable=False)
        tasks = relationship("Task", backref="projects", cascade='all, delete')
        resources = relationship("Resource", backref="projects", cascade='all, delete')
        submissions = relationship("Submission", backref="projects", cascade='all, delete')
    else:
        course_id = ""
        name = ""
        description = ""
        start = ""
        deadline = ""
        total_points = ""
        project_type = ""

    def __init__(self, *args, **kwargs):
        """initializes project"""
        super().__init__(*args, **kwargs)