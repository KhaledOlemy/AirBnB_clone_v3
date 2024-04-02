#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage2(unittest.TestCase):
    """test doc doc"""
    def test_get(self):
        """test doc doc"""
        state1 = State(name="dummyState1")
        state2 = State(name="dummyState2")
        state3 = State(name="dummyState3")
        state4 = State(name="dummyState4")
        models.storage.new(state1)
        models.storage.new(state2)
        models.storage.new(state3)
        models.storage.new(state4)
        models.storage.save()
        models.storage.close()
        dummy_state = list(models.storage.all().values())[0]
        dummy_state_id = dummy_state.id
        get = models.storage.get(State, dummy_state_id)
        self.assertEqual(get.id, dummy_state_id)
        models.storage.delete(get)
        models.storage.save()
        models.storage.close()
        get = models.storage.get(State, dummy_state_id)
        self.assertEqual(get, None)


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage3(unittest.TestCase):
    """test doc doc"""
    def test_count(self):
        """test doc doc"""
        state1 = State(name="dummyState1")
        state2 = State(name="dummyState2")
        state3 = State(name="dummyState3")
        state4 = State(name="dummyState4")
        city1 = State(name="dummyCity1", state_id=state1.id)
        city2 = State(name="dummyCity2", state_id=state2.id)
        city3 = State(name="dummyCity3", state_id=state3.id)
        city4 = State(name="dummyCity4", state_id=state4.id)
        models.storage.new(state1)
        models.storage.new(state2)
        models.storage.new(state3)
        models.storage.new(state4)
        models.storage.new(city1)
        models.storage.new(city2)
        models.storage.new(city3)
        models.storage.new(city4)
        models.storage.save()
        models.storage.close()
        total_count = len(models.storage.all())
        total_count_cp = models.storage.count()
        total_count_state = len(models.storage.all(State))
        total_count_state_cp = models.storage.count(State)
        total_count_city = len(models.storage.all(City))
        total_count_city_cp = models.storage.count(City)
        self.assertEqual(total_count, total_count_cp)
        self.assertEqual(total_count_state, total_count_state_cp)
        self.assertEqual(total_count_city, total_count_city_cp)
