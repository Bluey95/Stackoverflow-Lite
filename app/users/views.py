from flask import Flask, request, flash, redirect, url_for, jsonify, session
from . import user_api
from .models import User
import re
userObject = User() 

def validate_data(data):
    """validate user details"""
    try:
        # check if the username is more than 3 characters
        if len(data['username'].strip()) < 3:
            return "username must be more than 3 characters"
        elif not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+$", data['email'].strip()):
            return "please provide a valid email"
        # check if password has space
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

        print('gjfkdjgfk')
        data = request.get_json()
        print("here")
        res = validate_data(data)
        print(res)
        if res == "valid":
            email = data['email']
            username = data['username']
            password = data['password']
            user = User(username, email, password)
            response = user.create()
            return response
        return jsonify({"message":res}), 400


@user_api.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    user_details = request.get_json()
    
    try:
        print("hello")
        user = userObject.get_user_by_username(user_details['username'])
        print("here")
        if user and userObject.verify_password(user_details['password'], user['password']):
            return jsonify({"user": user, "message": "Login Successfull."}), 201
        else:
            # no user found, return an error message
            response = {'message': 'invalid username or password, Please try again'}
            return jsonify(response), 401
    except Exception as error:
        response = {'message': str(error)}
        return jsonify(response), 401

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