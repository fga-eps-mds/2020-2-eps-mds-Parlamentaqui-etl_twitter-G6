from flask import Blueprint
from models import *
from operator import attrgetter
import json

api = Blueprint('api', __name__, url_prefix='/api')

#@api.route('/tweets')
#def index():
#   tweets = ''
#    for item in Tweet.objects:
#        tweets = tweets + ' ' + item.twitter_username
#
#    return tweets



@api.route('/tweets')
def tweets():
    
    all_tweet = Tweet.objects

    sorted_list = sorted(all_tweet, key=attrgetter('date'))
    tweet_1 = sorted_list[0].to_json(sorted_list[0])
    tweet_2 = sorted_list[1].to_json(sorted_list[1])
    tweet_3 = sorted_list[2].to_json(sorted_list[2])
    tweet_4 = sorted_list[3].to_json(sorted_list[3])
    tweet_5 = sorted_list[4].to_json(sorted_list[4])
    tweet_6 = sorted_list[5].to_json(sorted_list[5])
    
    json_full={
        'tweets_01': tweet_1,
        'tweets_02': tweet_2,
        'tweets_03': tweet_3,
        'tweets_04': tweet_4,
        'tweets_05': tweet_5,
        'tweets_06': tweet_6
    }

    return json_full