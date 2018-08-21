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

    def filter_by_id(self, id):
        for question in self.question_list:
            if question['questionid'] == id:
                return jsonify(question)
            return jsonify("Question with that id does not exist.")
        return jsonify("error")

    def add_answer(self, qid, comment, upvote=0, downvote=0):
        self.answer = {}
       
        self.id = len(self.answer)
        self.answer['id'] = self.id + 1
        self.answer['qid'] = qid
        self.answer['comment'] = comment
        self.answer['upvote'] = upvote
        self.answer['downvote'] = downvote
        self.answer_list.append(self.answer)
        return jsonify(self.answer)
        