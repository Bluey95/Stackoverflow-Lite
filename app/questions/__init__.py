from flask import Blueprint
from flask_cors import CORS, cross_origin

api = Blueprint('api', __name__)
CORS(api)

from . import views
