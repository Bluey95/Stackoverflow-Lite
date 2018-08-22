import unittest
import os
import json
from flask import url_for, abort, session
from app import create_app

class TestViews(unittest.TestCase):

    def setUp(self):
        config_name = 'testing'
        app = create_app(config_name)
        self.client = app.test_client()
        self.register_user = json.dumps(dict(username="tests", password='pass123',
                    confirmpass='pass123'))
        self.client.post('api/v1/auth/registration',
                data = self.register_user, content_type='application/json')
        self.client.post('api/v1/auth/login', data=json.dumps(dict(username="tests", password='pass123'
                                                                                 )), content_type='application/json')
    
    def test_post_answer(self):
        """
        Test users can post answers
        """
        resource = self.client.post('/api/v1/questions/1/answer', data=json.dumps(dict(id=1, title="Blue Chronicles", body="Why blue is awesome?", comment="Because blue is just perfect")), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)

    def test_retrieve_answers(self):
        """
        Test users can retrieve all questions
        """
        self.client.post('/api/v1/questions/1/answer', data=json.dumps(dict(title="Blue Chronicles", body="Why blue is awesome?", comment="Because blue is just perfect")), content_type='application/json')                                                                                                                       # Retrieve Questions
        resource = self.client.get('/api/v1/questions/1/answer', data = json.dumps(dict(title="Blue Chronicles", body="Why blue is awesome?", comment="Because blue is just perfect")), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code,405)

    def test_empty_answer(self):
        """"
        Test for missing answer
        """
        resource = self.client.post('/api/v1/questions/1/answer', data=json.dumps(dict(comment="")), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code,200)
        self.assertEqual(resource.content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()
