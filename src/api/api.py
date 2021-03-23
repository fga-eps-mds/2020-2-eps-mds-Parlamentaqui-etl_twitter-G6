from flask import Blueprint
from models import *

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/tweets')
def index():
    tweets = ''
    for item in Tweet.objects:
        tweets = tweets + ' ' + item.twitter_username

@api.route('/test')
def test():
    message = ''
    for item in DBTest.objects:
        message = message + ' ' + item.message

    return message
