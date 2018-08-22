from flask import Flask, request, flash, redirect, url_for, jsonify, session
from . import api
from .models import Question
questionObject = Question() 

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
        if 'username' in session:
            data = request.get_json()
            res = validate_data(data)
            if res == "valid":
                title = data['title']
                body = data['body']
                response = questionObject.create(title, body)
                return response
            return jsonify({"message":res}), 422
        return jsonify({"message": "Please login to post a question."})
    data = questionObject.get_question()
    return data

@api.route('/questions/<int:id>', methods=["GET", "POST"])
def question_id(id):
    """ Method to create and retrieve a specific question."""
    data = questionObject.filter_by_id(id)
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