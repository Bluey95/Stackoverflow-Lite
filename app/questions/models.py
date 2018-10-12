from flask import jsonify, g
import json
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
        return jsonify({"message": "Successful", "question": self.fetch_by_id(questionid)}), 201
    
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

    def fetch_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM questions WHERE id = %s;", (id,))
        question = cur.fetchone()
        if question:
            return self.question_serialiser(question)
        return False

    def fetch_question_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM questions WHERE id = %s;", (id,))
        question = cur.fetchone()
        ans = Answer()
        answers = ans.fetch_answers_by_question_id(id)
        if question:
            return jsonify({"Question":self.question_serialiser(question), "Answers":answers})
        return False

    def fetch_question_by_userid(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM questions WHERE user_id = %s;", (id,))
        print("currently here")
        questions_tuple = cur.fetchall()
        questions = []
        
        if len(questions_tuple) > 0:
            for question in questions_tuple:
                """append questions after serializing to the list"""
                questions.append(self.question_serialiser(question))
            return jsonify({"Question":questions})
        return jsonify({"Message":"You have not posted any questions"})
    
    def is_owner(self, question_id, userid):
        """To check if question belong to the user"""
        cur.execute(
            "SELECT * FROM questions WHERE id=%s", (question_id, ))
        request_tuple = cur.fetchone()
        if request_tuple[4] == userid:
            return True
        return False

    def update(self, question_id):
        cur.execute("UPDATE questions SET title = %s, body = %s, created_by = %s, user_id = %s \
                WHERE id = %s;", (self.title, self.body, g.username, g.userid, question_id)
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
    def __init__(self, body=None, question_id=None, votes=None): 
        super(Answer, self).__init__()
        self.body = body
        self.question_id = question_id
        self.votes = 0

    def save(self):
        conn.commit()

    def create(self):
        """Create Answers"""
        answered_by = g.username
        user_id = g.userid
        question_id = self.question_id
        is_accepted = False
        cur.execute(
                """
                INSERT INTO answers (body, answered_by, user_id, question_id, is_accepted)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """,
            (self.body, answered_by, user_id, self.question_id, is_accepted))
        """fetch the new Answer, pick the id, and assign to questionid"""
        questionid = cur.fetchone()[0]
        """save Answer"""
        self.save()
        question = Question()
        return question.fetch_question_by_id(question_id), 201

    def fetch_answers_by_question_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT *, (Select COUNT(*) from votes where votes.answer_id=answers.id AND votes.vote=True) as upvotes, (Select COUNT(*) from votes where votes.answer_id=answers.id AND votes.vote=False) as downvotes FROM answers WHERE question_id = %s;", (id,))
        answers_tuple = cur.fetchall()
        answers = []

        if len(answers_tuple) > 0:
            for answer in answers_tuple:
                """append answers after serializing to the list"""
                answers.append(self.answers_serialiser(answer))
            return answers
        return answers_tuple

    def fetch_answer_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT *,  (Select COUNT(*) from votes where votes.answer_id=%s AND votes.vote=True) as upvotes, (Select COUNT(*) from votes where votes.answer_id=%s AND votes.vote=False) as downvotes FROM answers WHERE id = %s;", (id, id, id))
        answer = cur.fetchone()
        if answer:
            return jsonify({"Answer":self.answers_serialiser(answer)})
        return False

    def fetch_answer(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM answers WHERE id = %s;", (id,))
        answer = cur.fetchone()
        if answer:
            return answer
        return False

    def is_owner(self, answer_id, userid):
        """To check if answer belong to the user"""
        cur.execute(
            "SELECT * FROM answers WHERE id=%s", (answer_id, ))
        request_tuple = cur.fetchone()
        if request_tuple[4] == userid:
            return True
        return False

    def update(self, answer_id):
        res = self.fetch_answer(answer_id)
        if res:
            is_accepted = False
            question_id = res[3]
            cur.execute("UPDATE answers SET body = %s, answered_by = %s, user_id = %s, \
            question_id = %s, is_accepted = %s, votes = %s WHERE id = %s;", 
                (self.body, g.username, g.userid, question_id, is_accepted, self.votes, answer_id)
)
            item = self.fetch_answer(answer_id)
            self.save()
            return jsonify({"message": "Update succesfful", "response": self.answers_serialiser(item)}), 201
        return jsonify({"message": "Sorry the answer with this id doesnt exist."}), 404

    def delete_answer(self, answer_id):
        cur.execute(
            "DELETE FROM answers WHERE id=%s", (answer_id, ))
        self.save()
        return "Deleted Successfully"

    def accept(self, answer_id):
        res = self.fetch_answer(answer_id)
        if res:
            is_accepted = True
            question_id = res[3]
            user_id = res[4]
            body = res[1]
            answered_by = res[2]
            cur.execute("UPDATE answers SET body = %s, answered_by = %s, user_id = %s, \
                    question_id = %s, is_accepted = %s WHERE id = %s;", (body, answered_by, 
                        user_id, question_id, is_accepted, answer_id)
            )
            item = self.fetch_answer(answer_id)
            self.save()
            return jsonify({"message": "Update succesfful", 
                "response": self.answers_serialiser(item)}), 201
        return jsonify({"message": "Sorry the answer with this id doesnt exist."}), 404
    
    def is_upvoted(self, answer_id):
        cur.execute(""" SELECT * FROM votes WHERE answer_id=%s and vote=True and voted_by=%s""",(answer_id, g.username))
        res = cur.fetchall()
        if len(res) >= 1:
            return True

    def is_downvoted(self, answer_id):
        cur.execute(""" SELECT * FROM votes WHERE answer_id=%s and vote=False and voted_by=%s""",(answer_id, g.username))
        res = cur.fetchall()
        if len(res) >= 1:
            return True

    def upvote(self, answer_id):
        if self.is_upvoted(answer_id):
            return jsonify({"message": "you already voted"})
        res = self.fetch_answer(answer_id)
        if res:
            cur.execute(
                """
                INSERT INTO votes (voted_by, answer_id, vote)
                VALUES (%s, %s, %s) RETURNING id;
                """,
            (g.username, answer_id, True))
            item = self.fetch_answer(answer_id)
            self.save()
            return jsonify({"message": "upvote successful"}), 201
        return jsonify({"message": "Sorry the answer with this id doesnt exist."}), 404

    def downvote(self, answer_id):
        if self.is_downvoted(answer_id):
            return jsonify({"message": "you already voted"})
        res = self.fetch_answer(answer_id)
        if res:
            cur.execute(
            """
            INSERT INTO votes (voted_by, answer_id, vote)
            VALUES (%s, %s, %s) RETURNING id;
            """,
            (g.username, answer_id, False))
            item = self.fetch_answer(answer_id)
            self.save()
            return jsonify({"message": "downvote successful"}), 201
        return jsonify({"message": "Sorry the answer with this id doesnt exist."}), 404
    
    def question_with_most_answers(self):
        cur.execute(
            """SELECT Q.id, Q.title, Q.body, U.username,
                                             (SELECT COUNT(A.question_id) FROM answers A WHERE A.question_id = Q.id) as answercount
                                             FROM questions Q
                                             INNER JOIN users U ON Q.user_id = U.id
                                             INNER JOIN answers A ON A.question_id = Q.id
                                             GROUP BY A.question_id ,Q.id, U.username
                                              ORDER BY answercount DESC                                                     
                                                ;""")
        res = cur.fetchall()
        most_question_list = []
        for item in res:
            most_question_list.append({"question_id":item[0], "answers":item[4], "question_title":item[1], "question_body":item[2], "asked_by":item[3]})
        return jsonify({"Questions":most_question_list})

    def answers_serialiser(self, answer):
        """ Serialize tuple into dictionary """
        answer_details = dict(
            id=answer[0],
            question_id=answer[3],
            body=answer[1],
            answered_by=answer[2],
            user_id=answer[4],
            is_accepted=answer[5],
            upvotes=answer[6],
            downvotes=answer[7]
        )
        return answer_details