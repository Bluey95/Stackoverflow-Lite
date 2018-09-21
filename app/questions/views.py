from flask import Flask, request, flash, redirect, url_for, jsonify, session, abort, render_template, g
from . import api
from .models import Question, Answer
import re
from app.users.models import User
from app.jwtfile import Jwt_details
from flask_cors import CORS, cross_origin
questionObject = Question()
answerObject = Answer() 
jwt_obj = Jwt_details()

@api.before_app_request
def before_request():
    """get the user bafore every request"""
    if request.endpoint and 'auth' not in request.url:

        try:
            if request.method != 'GET':
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
        elif " " in data['title']:
            return ("Only one key word is allowed.")
        elif not re.match("^[A-Za-z]*$", data['title']):
            return ("Invalid title. Your title should only contain letters")
        elif " " in data['title']:
            return ("Only one key word is allowed.")
        elif len(data['body'].strip()) == 0:
            return "Question body cannot be empty"
        elif len(data['body'].strip()) < 10:
            return "Try to be more descriptive."
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

def validate_answers_data(data):
    """validate request details"""
    try:
        # check if title more than 10 characters
        if len(data['body'].strip()) == 0:
            return "Answer body cannot be empty"
        elif len(data['body'].strip()) < 10:
            return "Try to be more descriptive."
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@api.route('/questions', methods=["GET", "POST"])
@cross_origin()
def question():
    """ Method to create and retrieve questions."""
    try:
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
        data = questionObject.get_all_questions()
        return data
    except Exception:
        return jsonify({"message": "Bad JSON object"}), 400

@api.route('/questions/<int:id>', methods=["GET", "PUT"])
@cross_origin()
def question_id(id):
    """ Method to retrieve and update a specific question."""
    if request.method == 'PUT':
        try:
            data = request.get_json()
            check_details = validate_data(data)
            if check_details is not "valid":
                return jsonify({"message": check_details}), 400
            else:
                if questionObject.fetch_question_by_id(id) is False:
                    return jsonify({"message": "The Question with that ID doesnt exist"}), 404
                else:
                    if questionObject.is_owner(id, g.userid) is False:
                        return jsonify({"message": "Sorry you cant edit this question"}), 401
                    else:
                        try:
                            title = data['title']
                            body = data['body']
                            req = Question(title, body)
                            res = req.update(id)
                            return jsonify({"message": "Update succesfful"}), 201, {'Access-Control-Allow-Origin': '*'}
                        except Exception as error:
                            # an error occured when trying to update request
                            response = {'message': str(error)}
                            return jsonify(response), 401
        except Exception:
            return jsonify({"message": "Bad JSON object"}), 400


    item = questionObject.fetch_question_by_id(id)
    if item is False:
        return jsonify({"message": "The question with the specified id does not exist"}), 404
    else:
        return item, 200

@api.route('/questions/<int:qid>/answer', methods=["POST"])
@cross_origin()
def answer(qid):

    """ Method to create and retrieve questions."""
    try:
        data = request.get_json()
        if questionObject.fetch_question_by_id(qid) is False:
            return jsonify({"message": "The Question with that ID doesnt exist"}), 404
        res = validate_answers_data(data)
        if res == "valid":
            body = data['body']
            ans = Answer(body, qid)
            res = ans.create()
            return res
        return jsonify({"message":res}), 422
    except Exception:
        return jsonify({"message": "Bad JSON object"}), 400


@api.route('/questions/<int:id>/answer/<int:ansid>', methods=["GET","PUT"])
@cross_origin()
def mark(id, ansid):

    """ Method to create a mark."""
    if request.method == "PUT": 
        try:
            if questionObject.fetch_question_by_id(id) is False:
                return jsonify({"message": "The Question with that ID doesnt exist"}), 404
            if questionObject.is_owner(id, g.userid) is True:
                res = answerObject.accept(ansid)
                return res
            elif answerObject.is_owner(ansid, g.userid) is True:
                data = request.get_json()
                res = validate_answers_data(data)
                if res == "valid":
                    body = data['body']
                    req = Answer(body)
                    res = req.update(ansid)
                    return res
                return jsonify({"message":res}), 422
            return jsonify({"message": "Sorry you are not allowed to update this answer."})
        except Exception:
            return jsonify({"message": "Bad JSON object"}), 400

    response = answerObject.fetch_answer_by_id(ansid)
    return response

@api.route('/questions/<int:id>/answer/<int:ansid>/upvote', methods=["PUT"])
@cross_origin()
def upvote_answer(id, ansid):

    """ Method to upvote."""
    request.method == "POST"
    if questionObject.fetch_question_by_id(id) is False:
        return jsonify({"message": "The Question with that ID doesn't exist"}), 404
    if answerObject.fetch_answer_by_id(ansid) is False:
        return jsonify({"message": "The Answer with that ID doesn't exist"}), 404
    if answerObject.is_owner(ansid, g.userid) is False:
        data = request.get_json()
        res = answerObject.upvote(ansid)
        return res
    return jsonify({"message": "You are not allowed to vote on your own answer"})

@api.route('/questions/<int:id>/answer/<int:ansid>/downvote', methods=["PUT"])
def downvote_answer(id, ansid):

    """ Method to downvote."""
    if questionObject.fetch_question_by_id(id) is False:
        return jsonify({"message": "The Question with that ID doesn't exist"}), 404
    if answerObject.fetch_answer_by_id(ansid) is False:
        return jsonify({"message": "The Answer with that ID doesn't exist"}), 404
    if answerObject.is_owner(ansid, g.userid) is False:
        request.method == "POST"
        data = request.get_json()
        res = answerObject.downvote(ansid)
        return res
    return jsonify({"message": "Are you really trying to downvote your own answer?"})

@api.route('/questions/mostanswers', methods=["GET"])
def most_answers():
    """ Method to retrieve question with most answers."""
    response = answerObject.question_with_most_answers()
    return response

@api.route('/questions/<int:id>', methods=["DELETE"])
def admin_delete(id):
    """ endpoint to delete questions"""
    question_exist = questionObject.fetch_question_by_id(id)
    if not question_exist:
        return jsonify(response="Question does not exist"), 404
    else:
        if questionObject.is_owner(id, g.userid) is False:
            return jsonify({"message": "Sorry you have no permission to delete this question"}), 401
        else:
            try:
                resp = questionObject.delete(id)
                return jsonify(response=resp), 200
            except Exception as error:
                # an error occured when trying to update request
                response = {'message': str(error)}
                return jsonify(response), 401

@api.route('/questions/<int:id>/answer/<int:ansid>', methods=["DELETE"])
def admin_delete_answer(id, ansid):
    """ endpoint to delete answers"""
    question_exist = questionObject.fetch_question_by_id(id)
    if not question_exist:
        return jsonify(response="Question does not exist"), 404
    else:
        answer_exist = answerObject.fetch_answer_by_id(ansid)
        if answerObject.is_owner(ansid, g.userid) is False:
            return jsonify({"message": "Sorry you have no permission to delete this answer"}), 401
        else:
            try:
                resp = answerObject.delete(ansid)
                return jsonify(response=resp), 200
            except Exception as error:
                # an error occured when trying to update request
                response = {'message': str(error)}
                return jsonify(response), 401


@api.route('/questions/myquestions', methods=["GET"])
def myquestions():
    """ Method to retrieve a specific user's questions."""
    item = questionObject.fetch_question_by_userid(g.userid)
    return item, 200


