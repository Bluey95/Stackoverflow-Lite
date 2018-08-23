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
        created_by = session["username"]
        user_id = session["userid"]
        cur.execute(
                """
                INSERT INTO questions (title, body, created_by, user_id)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (self.title, self.body, created_by, user_id))
        """fetch the new question, pick the id, and assign to questionid"""
        questionid = cur.fetchone()[0]
        """save question"""
        self.save()
        return jsonify({"message": "Successful", "question": self.fetch_question_by_id(questionid)}), 201
    
    def get_all_questions(self):
        """retrieve all users"""
        cur.execute("SELECT * FROM questions")
        """fetch all questions using cursor and assign results to questions_tuple"""
        questions_tuple = cur.fetchall()
        questions = []

        for question in questions_tuple:
            """append questions after serializing to the list"""
            questions.append(self.question_serializer(question))
        return jsonify({"QUestions": questions})

    def question_serialiser(self, question):
        """ Serialize tuple into dictionary """
        print()
        question_details = dict(
            id=question[0],
            title=question[1],
            body=question[2],
            created_by=created_by[3],
            user_id=user_id[4]
        )
        return question_details

    def fetch_question_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
        question = cur.fetchone()
        return self.question_serialiser(question)

