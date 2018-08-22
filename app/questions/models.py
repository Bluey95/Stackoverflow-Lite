import uuid
from flask import jsonify, session

class Question(object):
    def __init__(self):
        """ Initialize empty questions list"""  
        self.question_list = []
        self.answer_list = []

    def create(self, title, body):
        """Create questions"""
        self.questions = {}
        
        self.quiz_id = len(self.question_list)
        self.questions['title'] = title
        self.questions['body'] = body
        self.questions['userid'] = session['userid']
        self.questions['postedBy'] = session['username']
        self.questions['questionid'] = self.quiz_id + 1
        self.question_list.append(self.questions)
        return jsonify({"message": "Successful.", "question":self.question_list}), 201        

    def get_question(self):
       """ get questions """
       return jsonify({"Questions": self.question_list}), 200

    def get_question_by_id(self, id):
        for question in self.question_list:
            if question['questionid'] == id:
                ans = [answ for answ in self.answer_list if answ['qid'] == id]
                return jsonify({"Question":question, "Answer": ans})
            return jsonify("Question with that id does not exist.")
        return jsonify("Question with that id does not exist.")

    def add_answer(self, qid, comment, upvote=0, downvote=0):
        self.answer = {}
       
        self.id = len(self.answer)
        self.answer['id'] = self.id + 1
        self.answer['qid'] = qid
        self.answer['answerdBy'] = session['username']
        self.answer['comment'] = comment
        self.answer['upvote'] = upvote
        self.answer['downvote'] = downvote
        self.answer_list.append(self.answer)
        return jsonify(self.answer)

        