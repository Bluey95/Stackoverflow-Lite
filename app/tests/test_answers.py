import unittest
import os
import json
from flask import url_for, abort, session
from app import create_app
from migrate import create_questions_table, create_answers_table

class TestViews(unittest.TestCase):

    def setUp(self):
        config_name = 'testing'
        app = create_app(config_name)
        self.client = app.test_client()
        self.question = json.dumps(dict(title="Blue chronicles", body="Why blue is awesome?"))
        self.register_user = json.dumps(dict(username="susan", email="susan@info.co", password='pass123',
                    confirmpass='pass123'))
        self.client.post('api/v2/auth/registration',
                data = self.register_user, content_type='application/json')
        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="susan", password='pass123'
                                                                                 )), content_type='application/json')
        response = json.loads(resource.data.decode())
        access_token = response["Access_token"]
        Authorization='Bearer ' + access_token
        self.headers = {'content-type': 'application/json','Authorization': Authorization}
        
    def tearDown(self):
        create_questions_table()
        create_answers_table()
    
    def test_post_answer(self):
        """
        Test users can post answers
        """
        self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        resource = self.client.post('/api/v2/questions/1/answer', data=json.dumps(dict(body="its pretty")), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(data["Answers"][0]['body'], "its pretty")

    def test_retrieve_answers(self):
        """
        Test users can retrieve all answers belonging to a question
        """
        self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        self.client.post('/api/v2/questions/1/answer', data=json.dumps(dict(body="blue is prety")), headers=self.headers)                                                                                                                       # Retrieve Questions
        resource = self.client.get('/api/v2/questions/1', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code,200)
        self.assertEqual(len(data['Answers']),1)


if __name__ == '__main__':
    unittest.main()
