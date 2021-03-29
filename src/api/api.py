from flask import Blueprint, jsonify
from models import *
import requests
import os
import json

api = Blueprint('api', __name__, url_prefix='/api')
BEARER_TOKEN_TWITTER = os.getenv('BEARER_TOKEN')

# Token que autoriza a busca por dados na API do Twitter pelo protocolo OAuth 2.0 (somente infos publicas no Twitter)
auth_header = {"Authorization": "Bearer {}".format(BEARER_TOKEN_TWITTER)}

# @api.route('/tweets')
# def index():
#     tweets = ''
#     for item in Tweet.objects:
#         tweets = tweets + ' ' + item.twitter_username

@api.route('/tweets')
def index():
    tweets = []
    for item in Tweet.objects:
        tweets.append(item.to_json(item))

    return jsonify(tweets)

@api.route('/test')
def test():
    message = ''
    for item in DBTest.objects:
        message = message + ' ' + item.message

    return message

# Rota que retorna infos de usernames especificos listados
@api.route('/user_lookup')
def user_lookup_by_username():
    #Parametros de busca
    usernames = "usernames=ANAMARIABRAGA,varien"

    r = requests.get(f"https://api.twitter.com/2/users/by?{usernames}", headers=auth_header) # POde ser que esteja faltando o '&' no final dessa url
    
    return r.json()

# Rota que retorna até 10 tweets mais recentes do usuario indicado pelo seu id
@api.route('/historico_tweets')
def busca_historico_tweets():
    
    user_id = 36679967 #ID da Ana Maria Braga
    # user_id = 2244994945
    
    params = get_params()


    r = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets", headers=auth_header, params=params)
    
    return r.json()

# Pega parâmetros de informações que serão trazidas dos tweets
def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,possibly_sensitive,lang"} # Para adicionar mais campos, só precisa coloacar a virgula sem espaço e um/ou mais dos parametros listados dentro do metodo

# Rota que retorna um tweet especifico pelo seu id
@api.route('/tweets_por_ids')
def busca_historico_tweet_por_id():
    
    tweet_ids = "ids=1376612438313852930" #Para adicionar mais ids, basta colocar a virrgula e o id sem espaço entre eles
    params = get_params_2()

    r = requests.get(f"https://api.twitter.com/2/tweets?{tweet_ids}", headers=auth_header, params=params)
    
    return r.json()

# Pega parâmetros de informações que serão trazidas dos tweets (versao dessa rota)
def get_params_2():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,possibly_sensitive,lang"} # Para adicionar mais campos, só precisa coloacar a virgula sem espaço e um/ou mais dos parametros listados dentro do metodo


@api.route('/atualizar_tweets')
def atualizar_tweets():
    pass