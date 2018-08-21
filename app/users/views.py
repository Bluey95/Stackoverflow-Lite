from flask import Flask, request, flash, redirect, url_for, jsonify, session
from . import user_api
from .models import User
userObject = User() 

def validate_data(data):
    """validate user details"""
    try:
        # check if the username is more than 3 characters
        if len(data['username'].strip()) < 3:
            return "username must be more than 3 characters"
        # check if password has spacese
        elif " " in data["password"]:
            return "password should be one word, no spaces"
        elif len(data['password'].strip()) < 5:
            return "Password should have atleast 5 characters"
        # check if the passwords match
        elif data['password'] != data['confirmpass']:
            return "passwords do not match"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@user_api.route('/registration', methods=["POST"])
def reg():
    """ Method to create user account."""
    if request.method == "POST":
            data = request.get_json()
            res = validate_data(data)
            if res == "valid":
                username = data['username']
                password = data['password']
                response = userObject.create(username, password)
                return response
            return jsonify({"message":res}), 400


@user_api.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    data = request.get_json()
    username = data['username']
    password = data['password']
    res = userObject.login(username, password)
    return res 
    
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