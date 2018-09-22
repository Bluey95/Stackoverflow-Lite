import unittest
import os
import json
from flask import url_for, abort, session
from app import create_app
from migrate import create_questions_table

class TestViews(unittest.TestCase):

    def setUp(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        self.client = app.test_client()
        self.question = json.dumps(dict(id=1, title="chronicles", body="Why blue is awesome?"))
        self.register_user = json.dumps(dict(username="tests", email="susan@gmail.com", 
                password='Pass123', confirmpass='Pass123'))
        self.client.post('api/v2/auth/registration',
                data = self.register_user, content_type='application/json')
        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="tests", 
                        password='Pass123')), content_type='application/json')
        response = json.loads(resource.data.decode())
        access_token = response["Access_token"]
        Authorization='Bearer ' + access_token
        self.headers = {'content-type': 'application/json','Authorization': Authorization}
        
    def tearDown(self):
        create_questions_table()
    
    def test_create_question(self):
        """
        Test users can post questions
        """
        resource = self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(data["message"], "Successful")

    def test_delete_question(self):
        """
        Test users can delete a question
        """
        resource = self.client.post('/api/v2/questions', data=self.question, headers=self.headers)
        data = json.loads(resource.data.decode())
        resource = self.client.delete('/api/v2/questions/1', data=self.question, headers=self.headers)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)


    def test_retrieve_question(self):
        """
        Test users can retrieve all questions
        """
        self.client.post('/api/v2/questions', data=self.question, headers=self.headers)                                                                                                                      # Retrieve Questions
        resource = self.client.get('/api/v2/questions', data = self.question, 
                        headers=self.headers) 
        print(resource)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(len(data), 1)

    def test_retrieve_specific_question(self):
        """
        Test users can retrieve a specific question
        """     
        res = self.client.post('/api/v2/questions', data=self.question, headers=self.headers)                                                              
        resource = self.client.get('/api/v2/questions/1', data = self.question, headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(data['Question']['title'], "chronicles")

    def test_missing_title(self):
        """"
        Test for missing title
        """
        resource = self.client.post('api/v2/questions', data=json.dumps(dict(title="", 
                        body="Why blue is awesome?")), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Title cannot be empty')

    def test_missing_question_body(self):
        """"
        Test for missing question body
        """
        resource = self.client.post('api/v2/questions', data=json.dumps(dict(title="titles", body="")), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Question body cannot be empty')

    def test_title_should_only_contain_letters(self):
        """ Test that title should only contain letters """
        resource = self.client.post('api/v2/questions', data=json.dumps(dict(title="12vbkerue;", 
                        body="Why blue is awesome?")), headers=self.headers)

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Invalid title. Your title should only contain letters')

    def test_title_should_be_more_than_five_characters(self):
        """ Test that title should be more than five characters """
        resource = self.client.post('api/v2/questions', data=json.dumps(dict(title="titl;", 
                        body="Why blue is awesome?")), headers=self.headers)

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Title Must Be more than 5 characters')

    def test_title_should_be_more_than_five_characters(self):
        """ Test that title should have more than ten characters """
        resource = self.client.post('api/v2/questions', data=json.dumps(dict(title="titles", 
                        body="awesome?")), headers=self.headers)

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 422)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Try to be more descriptive.')


if __name__ == '__main__':
    unittest.main()
