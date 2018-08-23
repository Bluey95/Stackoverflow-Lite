import unittest
import os
import json
from flask import url_for, abort, session
from app import create_app

class TestViews(unittest.TestCase):

    def setUp(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        self.client = app.test_client()
        self.question = json.dumps(dict(title="Blue chronicles", body="Why blue is awesome?"))
        self.register_user = json.dumps(dict(username="tests", password='pass123',
                    confirmpass='pass123'))
        self.client.post('api/v2/auth/registration',
                data = self.register_user, content_type='application/json')
        self.client.post('api/v2/auth/login', data=json.dumps(dict(username="tests", password='pass123'
                                                                                 )), content_type='application/json')
        
    def tearDown(self):
        del self.question
    
    def test_create_question(self):
        """
        Test users can post questions
        """
        resource = self.client.post('/api/v2/questions', data=self.question, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(data["message"], "Successful.")

    def test_retrieve_question(self):
        """
        Test users can retrieve all questions
        """
        self.client.post('/api/v2/questions', data=self.question, content_type='application/json')                                                                                                                       # Retrieve Questions
        resource = self.client.get('/api/v2/questions', data = self.question, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(len(data['Questions']), 2)

    def test_retrieve_specific_question(self):
        """
        Test users can retrieve a specific question
        """                                                                    
        resource = self.client.get('/api/v2/questions/1', data = self.question, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(data['Question']['title'], "Blue chronicles")

    def test_missing_title(self):
        """"
        Test for missing title
        """
        resource = self.client.post('api/v2/questions', data=json.dumps(dict(title="", body="Why blue is awesome?")), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Title cannot be empty')

    def test_missing_question_body(self):
        """"
        Test for wrong login credentials
        """
        resource = self.client.post('api/v2/questions', data=json.dumps(dict(title="titles", body="")), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Question body cannot be empty')


if __name__ == '__main__':
    unittest.main()
