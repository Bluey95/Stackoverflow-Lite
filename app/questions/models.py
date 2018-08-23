import uuid
from flask import jsonify, session
import re
import psycopg2
from datetime import date, datetime
from connect import conn
from passlib.hash import sha256_crypt
cur = conn.cursor()

class Question(object):
    def __init__(self, title=None, body=None): 
        super(Question, self).__init__()
        self.title = title
        self.body = body

    def save(self):
        conn.commit()

    def create(self):
        """Create questions"""
        cur.execute(
                """
                INSERT INTO questions (title, body)
                VALUES (%s, %s) RETURNING id;
                """,
                (self.title, self.body))
            """fetch the new question, pick the id, and assign to questionid"""
            questionid = cur.fetchone()[0]
            """save question"""
            self.save()
            return jsonify({"message": "Successful", "question": self.question_by_id(questionid)}), 201
        
    def get_all_questions(self):
        """retrieve all users"""
        cur.execute("SELECT * FROM questions")
        """fetch all questions using cursor and assign results to questions_tuple"""
        questions_tuple = cur.fetchall()
        questions = []

        for question in questions_tuple:
            """append questions after serializing to the list"""
            questions.append(self.serializer(question))
        return jsonify({"QUestions": questions})


    def get_question_by_title(self, title):
        """retrieve a specific question"""
        cur.execute(
            "SELECT * FROM questions where title=%s", (title))
        question = cur.fetchone()
        if question:
            return self.serializer(question)
        return False

    def serializer(self, question):
        return dict(
            id=question[0],
            title=question[1],
            body=question[2]
        )

    def serialiser_question(self, question):
        """ Serialize tuple into dictionary """
        print()
        question_details = dict(
            id=question[0],
            title=question[1],
            body=question[2],
        )
        return question_details

    def question_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
        user = cur.fetchone()

    return self.serialiser_question(question)