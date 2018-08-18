from flask import Flask, request, flash, redirect, url_for, jsonify
import unittest
from models import Question


class Question_tests(unittest.TestCase):
    def setUp(self):
        """ set up global object before each test """
        self.question = Question()

    def tearDown(self):
        """ clear up global object after each test """
        del self.question

    def test_post_question(self):
        """ test that can create a question """
        response = self.question.create(title = "blue", body = "Is green better?")
        self.assertEqual(response[0]["title"], "blue")

    

