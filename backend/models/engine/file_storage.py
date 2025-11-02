#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import models
from models.base_model import BaseModel
from models.user import User
from models.course import Course
from models.project import Project
from models.submission import Submission
from models.test_case import TestCase
from models.test_result import TestResult
from models.task import Task
from models.resource import Resource
from models.level import Level
from models.event import Event
from models.grade import Grade
from models.timetable import Timetable
from models.draft import Draft

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Course": Course,
    "Project": Project,
    "Submission": Submission,
    "TestCase": TestCase,
    "TestResult": TestResult,
    "Task": Task,
    "Resource": Resource,
    "Level": Level,
    "Event": Event,
    "Grade": Grade,
    "Timetable": Timetable,
    "Draft": Draft,
}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects
    
    def search(self, cls, attributes):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception as e:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """method to retrieve one object Returns the object
        based on the class and its ID, or None if not found"""
        objs = models.storage.all(cls)
        for value in objs.values():
            if value.id == id:
                return value
        return None

    def count(self, cls=None):
        """method to count the number of objects in storage
        Returns the number of objects in storage matching
        the given class.
        If no class is passed, returns the count of all
        objects in storage"""
        if cls is not None:
            objs = models.storage.all(cls).values()
            count = len(objs)
        else:
            count = 0
            for cls in classes:
                objs = models.storage.all(cls).values()
                count += len(objs)
        return count
    
    def search(self, cls, attributes: dict = {}):
        """ Search all objects with matching attributes
        
        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                if (getattr(obj, k) != v):
                    return False
            return True
        
        return list(filter(_search, self.__objects[cls].values()))"""
        return [
            obj for obj in self.__objects[cls]
            if all(obj.get(key) == value for key, value in attributes.items())
        ]