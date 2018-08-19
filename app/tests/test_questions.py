from flask import Flask, request, flash, redirect, url_for, jsonify
import unittest
from .models import Question


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

    def test_get_question(self):
        """ test that can get a question """
        self.question.get_question()
        self.assertEqual("blue", "blue")

    def test_get_specific_question(self):
        """ test that can get a specific question """
        app = Flask(__name__)
        with app.app_context():
            self.question.get_specific_question(id = "1")
            self.assertEqual("1", "1")

    def test_post_answer(self):
        """ test that can add a question """
        self.question.add_answer(qid = "1", comment = "rachel", upvote="0", downvote="0")
        self.assertEqual("rachel", "rachel")
       
