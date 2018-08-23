import unittest
import os
import json
from flask import url_for, abort, session
from app import create_app
from migrate import create_users_table

class TestViews(unittest.TestCase):

    def setUp(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        self.register_user = json.dumps(dict(username="tests", email="susan@gmail.com", password='pass123',
                    confirmpass='pass123'))

        self.client = app.test_client()
        self.client.post('api/v2/auth/registration',
                data = self.register_user, content_type='application/json')

    def tearDown(self):
        create_users_table()


    def test_registration(self):
        """ Test for user registration """
        resource = self.client.post('api/v2/auth/registration',
                data = json.dumps(dict(username="test", email="susans@gmail.com", password='pass123',
                    confirmpass='pass123')), content_type='application/json')

        data = json.loads(resource.data.decode())
        print(data)
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Successful')

    def test_invalid_password(self):
        """ Test for invalid password """
        resource = self.client.post('api/v2/auth/registration',
                data=json.dumps(dict(username="test", email="susan@gmail.com", password='pas', confirmpass='pas')), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Password should have atleast 5 characters')

    def test_not_matching_password(self):
        """ Test for not matching password """
        resource = self.client.post('api/v2/auth/registration', data=json.dumps(dict(username="test", email="susan@gmail.com", password='pass123', confirmpass='pass1234'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'passwords do not match')

    def test_valid_username(self):
        """ Test for valid usernames """
        resource = self.client.post('api/v2/auth/registration', data=json.dumps(dict(username="te", email="susan@gmail.com", password='pass123', confirmpass='pass1234'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'username must be more than 3 characters')

    def test_valid_email(self):
        """ Test for valid email """
        resource = self.client.post('api/v2/auth/registration', data=json.dumps(dict(username="test", email="susan", password='pass123', confirmpass='pass1234'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'please provide a valid email')

    def test_for_existing_email(self):
        """ Test for existing email. """
        resource = self.client.post('api/v2/auth/registration', data=json.dumps(dict(username="test", email="susan@gmail.com", password='pass123', confirmpass='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Email is already taken.')

    def test_login(self):
        """"
        Test for login
        """
        # Login the user
        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="tests", password='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        print(data)
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Login Successfull.')

    def test_login_wrong_password(self):
        """"
        Test for wrong login credentials
        """
        # Login user
        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="tests", password='pass12'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'invalid username or password, Please try again')
    

if __name__ == '__main__':
    unittest.main()
