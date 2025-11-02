#!/usr/bin/python3
""" holds class User"""
import hashlib
from datetime import datetime
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import relationship



class User(BaseModel, Base):
    """Representation of a user """
    if storage_t == 'db':
        __tablename__ = 'users'
        title = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        _password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        matric_number = Column(String(128), nullable=True)
        role = Column(Enum('student', 'instructor', 'admin', name='user_roles'), nullable=False)
        level_id = Column(String(128), ForeignKey('levels.id', ondelete='CASCADE'), nullable=True)
        session_id = Column(String(128), nullable=True)
        reset_token = Column(String(128), nullable=True)
        submissions = relationship("Submission", backref="users", cascade='all, delete')
        grades = relationship("Grade", backref="users", cascade='all, delete')
        level = relationship('Level', back_populates='students')
        
        
        #task_result = relationship("TaskResult", backref="users")
    else:
        title = ""
        email = ""
        _password = ""
        first_name = ""
        last_name = ""
        matric_number = ""
        role = ""
        level_id = ""
        session_id = ""
        reset_token = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self) -> str:
        """ Getter of the password
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password
    
    def is_valid_session_id(self, sessionId: str) -> bool:
        """ Validate a password
        """
        if sessionId is None or type(sessionId) is not str:
            return False
        if self.session_id is None:
            return False
        
        return sessionId == self.session_id

    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)