import uuid
from flask import jsonify
import re

class User(object):
    def __init__(self):
        """ Initialize empty user list"""  
        self.user_list = []

    def create(self, username, password, confirmpass):
        """Create users"""
        self.users = {}
        
        self.id = len(self.user_list)
        self.users['username'] = username
        self.users['password'] = password
        self.users['confirmpass'] = confirmpass
        self.users['userid'] = self.id + 1
        self.user_list.append(self.users)
        return self.user_list

    def login(self, username, password):
        for user in self.user_list:
            if username == user['username']:
                if password == user['password']:
                    return "successful"
                else:
                    return "wrong password"
            else:
                return "user does not exist", 200
        return "You are successfully logged in"

    def get_user(self):
       """ get users """
       return self.user_list

    def get_specific_user(self, id):
        """get specific user """
        user = [user for user in self.user_list if user['userid'] == id]
        return jsonify({"User": user})

    def valid_username(self, username):
		"""check username length and special characters"""
		if len(username) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", username):
			return False
		else:
			return True
            
    def valid_password(self, password):
        """check password length and special characters"""
        if len(password) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", password):
            return False
        else:
            return True
        
    

    
        