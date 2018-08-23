from flask import Flask, request, flash, redirect, url_for, jsonify, session, abort, render_template, g
from . import api
from .models import Question
from app.users.models import User
from app.jwtfile import Jwt_details
questionObject = Question() 
jwt_obj = Jwt_details()

@api.before_app_request
def before_request():
    """get the user bafore every request"""
    if request.endpoint and 'auth' not in request.url:

        try:
            if request.method != 'OPTIONS':
                auth_header = request.headers.get('authorization')
                g.user = None
                access_token = auth_header.split(" ")[1]
                res = jwt_obj.decode_auth_token(access_token)
                if isinstance(res, int) and not jwt_obj.is_blacklisted(access_token):
                    # check if no error in string format was returned
                    # find the user with the id on the token
                    user = User()
                    response = user.user_by_id(res)
                    g.userid = response['id']
                    g.username = response['username']
                    return
                return jsonify({"message": "Please register or login to continue"}), 401
        except Exception:
            return jsonify({"message": "Authorization header or acess token is missing."}), 400

def validate_data(data):
    """validate request details"""
    try:
        # check if title more than 10 characters
        if len(data['title'].strip()) == 0:
            return "Title cannot be empty"
        elif len(data['body'].strip()) == 0:
            return "Question body cannot be empty"
        elif len(data['title'].strip()) < 5:
            return "Title Must Be more than 5 characters"
        elif len(data['body'].strip()) < 10:
            return "Body must be more than 10 letters"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@api.route('/questions', methods=["GET", "POST"])
def question():
    """ Method to create and retrieve questions."""
    if request.method == "POST":
        data = request.get_json()
        res = validate_data(data)
        if res == "valid":
            title = data['title']
            body = data['body']
            question = Question(title, body)
            response = question.create()
            return response
        return jsonify({"message":res}), 422
    data = questionObject.get_question()
    return data

@api.route('/questions/<int:id>', methods=["GET", "POST"])
def question_id(id):
    """ Method to create and retrieve a specific question."""
    data = questionObject.get_question_by_id(id)
    return data


@api.route('/questions/<int:qid>/answer', methods=["POST"])
def answer(qid):

    """ Method to create and retrieve questions."""
    if 'username' in session:
        data = request.get_json()
        comment = data['comment']
        res = questionObject.add_answer(qid, comment)
        return res
    return jsonify({"message": "Please login to answer a question."})