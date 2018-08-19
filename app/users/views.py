from flask import Flask, request, flash, redirect, url_for, jsonify, session
from . import user_api
from config import DevelopmentConfig
from .models import User
userObject = User() 

@user_api.route('/registration', methods=["POST"])
def reg():
    """ Method to create user account."""
    if request.method == "POST":
            data = request.get_json()
            username = data['username']
            password = data['password']
            confirmpass = data['confirmpass']
            if len(password) < 5:
                return "Password too short"
            elif password != confirmpass:
                return "passwords do not match"
            for user in userObject.user_list:
                if not userObject.valid_username(username):
                    return "Username Not Valid"
                elif username == user['username']:
                    return "username already exists. Try another name."
               
            userObject.create(username, password, confirmpass)
            return jsonify({"message":"Dear " + username + " you have been succesfully registered."})

@user_api.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    data = request.get_json()
    for user in userObject.user_list:
        username = data['username']
        password = data['password']
        if not userObject.valid_username(username):
            return "Username Not Valid"
        else:
            if not userObject.valid_password(password):
                return "Password Not Valid"
        res = userObject.login(username, password)
        if res == "successful":
            if user['username'] == username and user['password'] == password:
                return jsonify(response ="login successful"), 200
    return jsonify({"message" : res })
    
@user_api.route('/users', methods=["GET"])    
def users():
    if request.method == "GET":
        data = userObject.get_user()
        return jsonify({"Users" : data})

@user_api.route('/users/<int:id>', methods=["GET", "POST"])
def user_id(id):
    """ Method to create and retrieve a specific user."""
    data = userObject.get_specific_user(id)
    return data