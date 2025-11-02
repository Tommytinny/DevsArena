#!/usr/bin/python3
""" holds class resource"""
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Resource(BaseModel, Base):
    """Representation of a Resource """
    if storage_t == 'db':
        __tablename__ = 'resources'
        project_id = Column(String(128), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
        title = Column(String(255), nullable=False)
        type = Column(String(50), nullable=False)
        url = Column(Text, nullable=False)
    else:
        project_id = ""
        title = ""
        type = ""
        url = ""

    def __init__(self, *args, **kwargs):
        """initializes resource"""
        super().__init__(*args, **kwargs)