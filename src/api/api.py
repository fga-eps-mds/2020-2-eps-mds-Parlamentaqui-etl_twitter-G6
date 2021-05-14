from flask import Blueprint, jsonify
from models import *
from unidecode import unidecode
from datetime import datetime
import requests
import os
from operator import attrgetter
import json

api = Blueprint('api', __name__, url_prefix='/api')
BEARER_TOKEN_TWITTER = os.getenv('BEARER_TOKEN')

# Token que autoriza a busca por dados na API do Twitter pelo protocolo OAuth 2.0 (somente infos publicas no Twitter)
auth_header = {"Authorization": "Bearer {}".format(BEARER_TOKEN_TWITTER)}

#TWEETS DE DEPUTADOS
@api.route('/tweets')
def tweets():
    sorted_list = []
    sorted_list = sorted(Tweet.objects, reverse=True, key=attrgetter('date'))

    all_tweet = []

    for item in sorted_list[0:4]:
        all_tweet.insert(0, item.to_json())
    
    return jsonify(all_tweet)

@api.route('/update_tweets')
def update_tweets():
    update_twitter_accounts()
    params = get_params_2()

    for deputy in Deputy.objects:
        
        if deputy.twitter_id:
            r = requests.get(f"https://api.twitter.com/2/users/{deputy.twitter_id}/tweets", headers=auth_header, params=params)

            if not r:
                continue
            
            last_10_tweets_json = r.json()['data']

            for tweet_json in last_10_tweets_json:
                
                old_tweet = Tweet.objects(tweet_id=tweet_json['id']).first()
                if old_tweet:
                    continue

                new_tweet = Tweet(
                    tweet_id = str(tweet_json['id']),
                    deputy_id = deputy.id,
                    name = deputy.name,
                    twitter_username = deputy.twitter_username,
                    date = datetime.strptime(str(tweet_json["created_at"][0:18]), '%Y-%m-%dT%H:%M:%S') if tweet_json["created_at"] is not None else None,
                    source = tweet_json['text']
                ).save()

                #criar a lógica de atualização da ultima atividade recente do deputado em questão
                deputy.last_activity_date = new_tweet.date
                deputy.save()

    return "Updated tweets sucessfully. Now use /get_all_tweets to see the tweets"

def update_twitter_accounts():
    for item in Deputy.objects:

        #verificar se o deputado já tem seu twitter vinculado, se tiver, só passa pro próximo
        if item.twitter_username or item.twitter_id:
            continue

        #criar as chaves para pesquisa
        deputy_name = item.name
        deputy_name = unidecode(deputy_name).replace(".", "").replace("'","").replace("-","").replace(" ", "")[0:13]

        deputy_full_name = item.full_name
        deputy_full_name = unidecode(deputy_full_name).replace(".", "").replace("'","").replace("-","").replace(" ", "")[0:13]

        usernames_to_found = deputy_name + "," + deputy_full_name
        r = requests.get(f"https://api.twitter.com/2/users/by?usernames={usernames_to_found}&user.fields=verified,url", headers=auth_header)

        #caso a resposta seja nula, ignorar esse deputado
        if not r:
            continue 

        deputy_twitter_json = r.json()

        # Criar uma String para conseguir verificar se ele possue a chave data
        json_in_string = str(deputy_twitter_json)
        
        # if deputy_twitter_json.optString("data"):
        if "data" in json_in_string:
            #encontramos um deputado com conta

            for all_usermaes_fouded in deputy_twitter_json["data"]:
                if all_usermaes_fouded["verified"]:
                    #conta verificada, adicionar no item
                    item.twitter_username = all_usermaes_fouded["username"]
                    item.twitter_id = all_usermaes_fouded["id"]
                    
                    if len(all_usermaes_fouded["url"]) > 5:
                        item.website = all_usermaes_fouded["url"]
                    
                    item.save()
                    break
    
    return "Done. Use url api/get_all_deputies for get all the deputies in db"

def get_params_2():
    return "tweet.fields=created_at,id,author_id,text"

@api.route('/get_all_deputies')
def get_all_deputies():
    t = []
    for item in Deputy.objects:
        t.append(item.to_json())

    return jsonify(t)

@api.route('/get_all_tweets')
def index():
    tweets = []
    sorted_list = sorted(Tweet.objects, reverse=True, key=attrgetter('date'))

    for item in sorted_list:
        tweets.append(item.to_json())

    return jsonify(tweets)

@api.route('/delete_all_tweets')
def delete_all_tweets():    
    Tweet.objects.all().delete()
    return "All tweets were deleted"


#TWEETS DE PROPOSIÇÕES
@api.route('/get_all_propositions')
def get_all_propositions():
    propositions = []
    for item in Proposicao.objects:
        propositions.append(item.to_json())

    return jsonify(propositions)

@api.route('/update_tweets_propositions')
def update_tweets_propositions():
    
    for item in Proposicao.objects:
        tweets_list = tweets_by_proposition_id(int(item.proposicao_id))
        
        for tweet in tweets_list:
            if "RT " in tweet["text"]:
                continue
                
            PropositionTweet(
                tweet_id = str(tweet["id"]),
                author_id = tweet["author_id"],
                proposition_id = item.proposicao_id,
                date = datetime.strptime(str(tweet["created_at"][0:18]), '%Y-%m-%dT%H:%M:%S') if tweet["created_at"] is not None else None,
                source = tweet["text"]
            ).save()

    return "Done. Use /get_all_tweets_propositions to get all the tweets that mentions proopsitions in data base."

@api.route('/get_all_tweets_propositions')
def get_all_tweets_propositions():
    all = []
    sorted_list = sorted(PropositionTweet.objects, reverse=True, key=attrgetter('date'))
    for item in sorted_list:
        all.append(item.to_json())

    return jsonify(all)

@api.route('/get_tweets_by_proposition_id/<id>')
def get_tweets_by_proposition_id(id):
    tweets = []
    sorted_list = sorted(PropositionTweet.objects, reverse=True, key=attrgetter('date'))
    for item in sorted_list:
        if int(item.proposition_id) == int(id):
            tweets.append(item.to_json())

    return jsonify(tweets)

@api.route('/delete_all_tweets_propositions')
def delete_all_tweets_propositions():
    PropositionTweet.objects.all().delete()
    return "All propositions tweets were deleted"

def tweets_by_proposition_id(id):
    proposition = Proposicao.objects(proposicao_id=id).first()
    if not proposition:
        return {}

    proposition_tweets = []
    
    proposition_number = str(proposition["numero"]) + "/" + str(proposition["ano"])
    key = proposition["sigla_tipo"].replace(" ", "_") + "_" + proposition_number

    params = get_params_2()
    r = requests.get(f'https://api.twitter.com/2/tweets/search/recent?query={key}&max_results=100', headers=auth_header, params=params)
    
    if not r:
        return {}
    
    if not "data" in r.json():
        return {}

    return r.json()["data"]


@api.route('/get_tweets_id_deputy/<id>')
def get_tweets_id_deputy(id):
    tweets = []
    sorted_list = sorted(Tweet.objects, reverse=True, key=attrgetter('date'))
    for item in sorted_list:
        if int(item.deputy_id) == int(id):
            tweets.append(item.to_json())

    return jsonify(tweets)