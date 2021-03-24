from flask import Blueprint, jsonify
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

@api.route('/atualizar_tweets')
def atualizar_tweets():
    all_deputies = []

    for item in Deputy.objects:
        all_deputies.append(item.to_json(item))

    return jsonify(all_deputies)

