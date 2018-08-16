from flask import Flask, request, flash, redirect, url_for, jsonify
from app import app
from .models import Question
questionObject = Question() 

@app.route('/api/v1/questions', methods=["POST"])
def questions():
    """ Method to create and retrieve questions."""
    if request.method == "POST":
            data = request.get_json()
            title = data['title']
            body = data['body']
            res = questionObject.create(title, body)
            if len(res) < 1:
                return jsonify({"message":"Error creating the question."})
            return jsonify({"response":res, "message":"Succesfull."})
    
