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

   
       




