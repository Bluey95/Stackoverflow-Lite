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
            for user in userObject.user_list:
                if username == user['username']:
                    return "username already exists. Try another name."
                elif len(password) < 5:
                    return "Password too short"
            userObject.create(username, password)
            return jsonify({"message":"Dear " + username + " you have been succesfully registered."})

@user_api.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    user_details = request.get_json()
    username = user_details['username']
    password = user_details['password']
    res = userObject.login(username, password)
    if res == "successful":
        for user in userObject.user_list:
            if user['username'] == username and user['password'] == password:
                return jsonify(response ="login successful"), 200
    return jsonify({"message" : res })
    
@user_api.route('/users', methods=["GET"])    
def users():
    if request.method == "GET":
        data = userObject.get_user()
        return jsonify({"Users" : data})