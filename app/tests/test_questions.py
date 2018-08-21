import unittest
import os
import json
from flask import url_for, abort, session
from Flask_Testing import TestCase
from app import create_app

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)

        return app

    # def setUp(self):
    #     self.app = create_app('testing')
    #     self.app_context = self.app.app_context()
    #     self.app_context.push()
    #     self.client = self.app.test_client

class TestViews(TestBase):
    """ Question Test Cases""" 
    def test_questions_endpoints(self):
        """
        Test users can post questions
        """
        # Register User
        self.client.post('api/v2/registration',
                data=json.dumps(dict(username="test", password='pass123',
                    confirmpass='pass123')), content_type='application/json')

        # Login user
        self.client.post('api/v2/login', data=json.dumps(dict(username="test", password='pass123'
                                                                                 )), content_type='application/json')

        # create Question
        resource = self.client.post('/api/v1/questions', data=json.dumps(dict(title="Blue chronicles", body="Why blue is awesome?"
                                                                                             )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(data["message"], "Successful.")

        """
        Test users can retrieve all questions
        """
        # create Questions
        self.client.post('/api/v1/questions', data=json.dumps(dict(title="Unit testing.", body="Why is unit testing important?"
                                                                                             )), content_type='application/json')                                                                                                                       # Retrieve Questions
        resource = self.client.get('/api/v1/questions', content_type='application/json')
        data = json.loads(resource.data.decode())
        print(data)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(len(data['Questions']), 2)

        """
        Test users can retrieve a specific question
        """                                                                     # Retrieve Question By id
        resource = self.client.get('/api/v1/questions/1', content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(data['Question']['title'], "Blue chronicles")

if __name__ == '__main__':
    unittest.main()