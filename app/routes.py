from flask import Flask, request, flash, redirect, url_for, jsonify
from app import app

@app.route('/')

@app.route('/index')
def index():
    
    return "Hello its working."

