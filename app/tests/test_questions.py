from flask import Flask, request, flash, redirect, url_for, jsonify
import unittest
import json
from ..questions.models import Question

class Question_tests(unittest.TestCase):
    def setUp(self):
        """ set up global object before each test """
        self.question = Question()

    def tearDown(self):
        """ clear up global object after each test """
        del self.question

    def create(self):
        """ create questions. """
        res = self.question.create(title = "blue", body = "Is green better?")
        return res

    def test_post_question(self):
        """ test that can create a question """
        response = self.create()
        self.assertEqual(response[0]["title"], "blue")

    def test_get_question(self):
        """ test that can get a question """
        self.create() # Create question
        res = self.question.get_question()
        self.assertEqual(len(res), 1)

    # def test_get_specific_question(self):
    #     """ test that can get a specific question """
    #     app = Flask(__name__)
    #     with app.app_context():
    #         self.create()
    #         res = self.question.filter_by_id(1)
    #         r = json.loads(res)
    #         self.assertEqual(r['title'], "blue")

    # def test_post_answer(self):
    #     """ test that can add a question """
    #     app = Flask(__name__)
    #     with app.app_context():
    #         self.create()
    #         r = self.question.add_answer(1, "rachel", 0, 0)
    #         self.assertEqual(r.get('comment'), 1)


       
       
