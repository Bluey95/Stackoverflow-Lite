import uuid
from flask import jsonify

class User(object):
    def __init__(self):
        """ Initialize empty user list"""  
        self.user_list = []

    def create(self, username, password):
        """Create users"""
        self.users = {}
        
        self.id = len(self.user_list)
        self.users['username'] = username
        self.users['password'] = password
        self.users['userid'] = self.id + 1
        self.user_list.append(self.users)
        return self.user_list

    

    
        