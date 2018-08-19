from flask import Flask, request, flash, redirect, url_for, jsonify
from . import api
from .models import Question
questionObject = Question() 

@api.route('/questions', methods=["GET", "POST"])
def question():
    """ Method to create and retrieve questions."""
    if request.method == "POST":
            data = request.get_json()
            title = data['title']
            body = data['body']
            res = questionObject.create(title, body)
            return jsonify({"message":"Succesfull."})
    elif request.method == "GET":
        data = questionObject.get_question()
        return jsonify({"Questions" : data})
    

@api.route('/questions/<int:id>', methods=["GET", "POST"])
def question_id(id):
    """ Method to create and retrieve a specific question."""
    data = questionObject.get_specific_question(id)
    return data


@api.route('/questions/<int:qid>/answer', methods=["POST"])
def answer(qid):

    """ Method to create and retrieve questions."""
    data = request.get_json()
    comment = data['comment']
    res = questionObject.add_answer(qid, comment)
    return jsonify({"message":"Succesfull."})