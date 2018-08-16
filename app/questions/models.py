import uuid

class Question(object):
    def __init__(self):
        """ Initialize empty questions list"""  
        self.question_list = []

    def create(self, title, body):
        """Create questions"""
        self.questions = {}
        
        self.quizId = len(self.question_list)
        self.questions['title'] = title
        self.questions['body'] = body
        self.questions['questionid'] = self.quizId + 1
        self.question_list.append(self.questions)
        return self.question_list
        

   