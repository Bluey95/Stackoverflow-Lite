import uuid
from flask import jsonify

class Question(object):
    def __init__(self):
        """ Initialize empty questions list"""  
        self.question_list = []
        self.answer_list = []
        #self.questionid = 0

    def create(self, title, body):
        """Create questions"""
        self.questions = {}
        
        self.quizId = len(self.question_list)
        self.questions['title'] = title
        self.questions['body'] = body
        self.questions['questionid'] = self.quizId + 1
        self.question_list.append(self.questions)
        return self.question_list
        
    def get_question(self):
       """ get questions """
       return self.question_list

    def get_specific_question(self, id):
        """get specific question """
        question = [question for question in self.question_list if question['questionid'] == id]
        ans = [answ for answ in self.answer_list if answ['qid'] == id]
        return jsonify({"Question": question, "Answers" : ans })
        