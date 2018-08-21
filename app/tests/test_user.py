import unittest
import os
import json
from flask import url_for, abort, session
from flask_testing import TestCase
from app import create_app

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)

        return app

class TestViews(TestBase):

    def test_registration(self):
        """ Test for user registration """
        resource = self.client.post('api/v2/registration',
                data=json.dumps(dict(username="tests", password='pass123',
                    confirmpass='pass123')), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Successful')

    def test_invalid_password(self):
        """ Test for invalid password """
        resource = self.client.post('api/v2/registration',
                data=json.dumps(dict(username="test", password='pas', confirmpass='pas')), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Password should have atleast 5 characters')

    def test_not_matching_password(self):
        """ Test for not matching password """
        resource = self.client.post('api/v2/registration', data=json.dumps(dict(username="test", password='pass123', confirmpass='pass1234'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'passwords do not match')

    def test_valid_username(self):
        """ Test for valid usernames """
        resource = self.client.post('api/v2/registration', data=json.dumps(dict(username="te", password='pass123', confirmpass='pass1234'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'username must be more than 3 characters')

    def test_login(self):
        """"
        Test for login
        """
        # Register a user first
        self.client.post('api/v2/registration',
                data=json.dumps(dict(username="test", password='pass123',
                    confirmpass='pass123')), content_type='application/json')
        # Login the user
        resource = self.client.post('api/v2/login', data=json.dumps(dict(username="test", password='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'You are successfully logged in')

    def test_login_wrong_password(self):
        """"
        Test for wrong login credentials
        """
        # Register user
        self.client.post('api/v2/registration',
                data=json.dumps(dict(username="test", password='pass123',
                    confirmpass='pass123')), content_type='application/json')

        # Login user
        resource = self.client.post('api/v2/login', data=json.dumps(dict(username="test", password='pass12'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Wrong username or password')
    
    
if __name__ == '__main__':
    unittest.main()