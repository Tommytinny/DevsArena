#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool
import models
from models.base_model import Base
from models.user import User
from models.course import Course
from models.project import Project
from models.task import Task
from models.resource import Resource
from models.test_case import TestCase
from models.test_result import TestResult
from models.submission import Submission
from models.grade import Grade
from models.event import Event
from models.timetable import Timetable
from models.level import Level


classes = {"User": User, "Course": Course, "Project": Project,
           "Task": Task, "Resource": Resource, "TestCase": TestCase,
           "TestResult": TestResult, "Event": Event, "Submission": Submission,
           "Level": Level, "Grade": Grade, "Timetable": Timetable}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = os.getenv('MYSQL_USER')
        passwd = os.getenv('MYSQL_PWD')
        host = os.getenv('MYSQL_HOST')
        db = os.getenv('MYSQL_DB')
        env = os.getenv('ENV')
        self.__engine = create_engine(
            f'mysql+pymysql://{user}:{passwd}@{host}/{db}',
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            )
        if env == "development":
            #Base.metadata.drop_all(self.__engine)
            v = ""

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    #if hasattr(obj, '_sa_instance_state'):
                        #delattr(obj, '_sa_instance_state')
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(sess_factory)
        self.__session = session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
        
    def get(self, cls, cls_id):
        """method to retrieve one object Returns the object
        based on the class and its ID, or None if not found"""
        objs = models.storage.all(cls)
        for value in objs.values():
            if value.id == cls_id:
                return value
        return None
    

    def search(self, cls, attributes):
        """ Search all objects with matching attributes
        """
        objs = self.all(cls).values()
        
        matching_objs = [
            obj for obj in objs
            if all(getattr(obj, key) == value for key, value in attributes.items())
        ]
        return matching_objs