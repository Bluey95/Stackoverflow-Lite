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
        self.question = json.dumps(dict(id = 1, title="chronicles", body="Why blue is awesome?"))
        self.register_user = json.dumps(dict(username="susan", email="susan@info.co", 
                                    password='Pass123', confirmpass='Pass123'))
        self.client.post('api/v2/auth/registration',
                data = self.register_user, content_type='application/json')
        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="susan", 
                            password='Pass123')), content_type='application/json')
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
        resource = self.client.post('/api/v2/questions/1/answer', data=json.dumps(dict(
                            body="its pretty")), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(data["Answers"][0]['body'], "its pretty")

    def test_delete_answer(self):
        """
        Test users can post answers
        """
        self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        resource = self.client.post('/api/v2/questions/1/answer', data=json.dumps(dict(
                            body="its pretty", id=1)), headers=self.headers)
        data = json.loads(resource.data.decode())
        print(data)
        resource = self.client.delete('/api/v2/questions/1/answer/1', data=json.dumps(dict(
                            body="its pretty")), headers=self.headers)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)

    def test_retrieve_answers(self):
        """
        Test users can retrieve all answers belonging to a question
        """
        self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        self.client.post('/api/v2/questions/1/answer', data=json.dumps(dict(body="blue is pretty")), 
                    headers=self.headers)                                                                                                                       # Retrieve Questions
        resource = self.client.get('/api/v2/questions/1', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code,200)
        self.assertEqual(len(data['Answers']),1)

    def test_missing_body(self):
        """"
        Test for missing answer body
        """
        self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        resource = self.client.post('api/v2/questions/1/answer', data=json.dumps(dict(body=" ")), 
                            headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Answer body cannot be empty')

    def test_body_should_have__atleast_10_characters(self):
        """ Test for invalid password """
        self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        self.question = json.dumps(dict(id = 1, title="chronicles", body="Why blue is awesome?"))
        resource = self.client.post('api/v2/questions/', data=self.question, headers=self.headers)
        resource = self.client.post('api/v2/questions/1/answer', data=json.dumps(dict(body="chrons")), 
                            headers=self.headers)

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Try to be more descriptive.')


if __name__ == '__main__':
    unittest.main()
