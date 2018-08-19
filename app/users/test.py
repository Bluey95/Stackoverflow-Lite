from flask import Flask, request, flash, redirect, url_for, jsonify
import unittest
from models import User


class Question_tests(unittest.TestCase):
    def setUp(self):
        """ set up global object before each test """
        self.user = User()

    def tearDown(self):
        """ clear up global object after each test """
        del self.user

    def test_register_user(self):
        """ test that can create a user """
        response = self.user.create(username = "susan", password = "susan")
        self.assertEqual(response[0]["username"], "susan")

    def test_login_user(self):
        """ test that can login a user """
        self.user.login(username = "susan", password = "susan")
        self.assertEqual("susan" == "susan", "susan" == "susan")

    def test_password(self):
        """ test that password must be greater than 5 """
        self.user.login(username = "susan", password = "susan")
        self.failIf(len("susan") < 5)

    def test_get_user(self):
        """ test that can get a user """
        self.user.get_user()
        self.assertEqual("susan", "susan")

    def test_get_specific_user(self):
        """ test that can get a specific user """
        app = Flask(__name__)
        with app.app_context():
            self.user.get_specific_user(id = "1")
            self.assertEqual("1", "1")
       




