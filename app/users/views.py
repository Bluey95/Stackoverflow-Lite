from flask import Flask, request, flash, redirect, url_for, jsonify, abort, render_template, g, json
from . import user_api
from .models import User
import re
from app.jwtfile import Jwt_details

userObject = User() 
jwt_obj = Jwt_details()

def validate_data(data):
    """validate user details"""
    try:
        # check if the username is more than 3 characters
        if len(data['username'].strip()) < 3:
            return "username must be more than 3 characters"
        elif not re.match("^[A-Za-z]*$", data['username']):
            return ("Your username should only contain letters")
        elif not re.match("[^@]+@[^@]+\.[^@]+", data['email'].strip()):
            return "please provide a valid email"
        # check if password has space
        elif " " in data["password"]:
            return "password should be one word, no spaces"
        elif re.search('[0-9]', data["password"]) is None:
            return "Make sure your password has a number in it"
        elif re.search('[A-Z]',data["password"]) is None: 
            return "Make sure your password has a capital letter in it"
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
        try: 
            data = request.get_json()
            res = validate_data(data)
            if res == "valid":
                email = data['email']
                username = data['username']
                password = data['password']
                user = User(username, email, password)
                new_user = user.create()
                return new_user
            else:
                return jsonify({"message": res}), 422
        except Exception:
            return jsonify({"message": "bad json object"}), 400


@user_api.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    try:
        user_details = request.get_json()
        
        try:
            user = userObject.get_user_by_username(user_details['username'])
            if user and userObject.verify_password(user_details['password'], user['password']):
                auth_token = jwt_obj.generate_auth_token(user["id"])
                return jsonify({"message": "Login Successfull.", "Access_token": str(auth_token)}), 201

            else:
                response = {'message': 'invalid username or password, Please try again'}
                return jsonify(response), 401
        except Exception:
            response = {'message': str(error)}
            return jsonify(response), 401
    except Exception:
        return jsonify({"message": "bad json object"}), 400

@user_api.route('/users', methods=["GET"])   
def users():
    try:
        if request.method == "GET":
            data = userObject.get_all_users()
            return data
    except Exception:
        return jsonify({"message": "bad json object"}), 400

@user_api.route('/users/<int:id>', methods=["GET"])
def user_id(id):
    """ Method to retrieve a specific user."""
    try:
        if request.method == "GET":
            data = userObject.user_by_id(id)
            return jsonify({"user": data})
    except Exception:
        return jsonify({"message": "bad json object"}), 400