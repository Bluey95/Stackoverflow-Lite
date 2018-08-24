from flask import jsonify, g
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
        created_by = g.username
        user_id = g.userid
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
            questions.append(self.question_serialiser(question))
        return jsonify({"Questions": questions})

    def question_serialiser(self, question):
        """ Serialize tuple into dictionary """
        question_details = dict(
            id=question[0],
            title=question[1],
            body=question[2],
            created_by=question[3],
            user_id=question[4]
        )
        return question_details

    def fetch_question_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM questions WHERE id = %s;", (id,))
        question = cur.fetchone()
        ans = Answer()
        answers = ans.fetch_answers_by_question_id(id)
        print(answers)
        if question:
            return jsonify({"Question":self.question_serialiser(question), "Answers":answers})
        return False
    
    def is_owner(self, question_id, userid):
        """To check if question belong to the user"""
        cur.execute(
            "SELECT * FROM questions WHERE id=%s", (question_id, ))
        request_tuple = cur.fetchone()
        if request_tuple[4] == userid:
            return True
        return False

    def update(self, question_id):
        cur.execute("UPDATE questions SET title = %s, body = %s, created_by = %s, user_id = %s WHERE id = %s;", (self.title, self.body, g.username, g.userid, question_id)
        )
        item = self.fetch_question_by_id(question_id)
        self.save()
        return item

    def delete(self, question_id):
        cur.execute(
            "DELETE FROM questions WHERE id=%s", (question_id, ))
        self.save()
        return "Deleted Successfully"

class Answer(object):
    def __init__(self, body=None, question_id=None): 
        super(Answer, self).__init__()
        self.body = body
        self.question_id = question_id

    def save(self):
        conn.commit()

    def create(self):
        """Create Answers"""
        answered_by = g.username
        user_id = g.userid
        question_id = self.question_id
        cur.execute(
                """
                INSERT INTO answers (body, answered_by, user_id, question_id)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (self.body, answered_by, user_id, self.question_id))
        """fetch the new Answer, pick the id, and assign to questionid"""
        questionid = cur.fetchone()[0]
        """save Answer"""
        self.save()
        question = Question()
        return question.fetch_question_by_id(question_id), 201

    def fetch_answers_by_question_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM answers WHERE question_id = %s;", (id,))
        answers_tuple = cur.fetchall()
        answers = []

        if len(answers_tuple) > 0:
            for answer in answers_tuple:
                """append answers after serializing to the list"""
                answers.append(self.answers_serialiser(answer))
            return answers
        return answers_tuple

    def answers_serialiser(self, answer):
        """ Serialize tuple into dictionary """
        answer_details = dict(
            id=answer[0],
            question_id=answer[3],
            body=answer[1],
            answered_by=answer[2],
            user_id=answer[4]
        )
        return answer_details