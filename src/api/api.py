from flask import Blueprint, jsonify
from models import *
from unidecode import unidecode
import requests
import os
import json

api = Blueprint('api', __name__, url_prefix='/api')
BEARER_TOKEN_TWITTER = os.getenv('BEARER_TOKEN')

# Token que autoriza a busca por dados na API do Twitter pelo protocolo OAuth 2.0 (somente infos publicas no Twitter)
auth_header = {"Authorization": "Bearer {}".format(BEARER_TOKEN_TWITTER)}

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

# Rota que faz uma requsição à API do Twitter e retorna os perfis que são verificados
@api.route('/perfis_deputados_verificados')
def encontra_perfis_verificados():
    
    # Separação de 100 usernames para cada requisição (já que existem 573 deputados no DB)
    usernames = ["usernames=","usernames=","usernames=","usernames=","usernames=","usernames="]

    cont = 0
    aux = 0

    # Recolhe os nomes dos deputados para colocar no paramêtro da requisição
    for item in Deputy.objects:
        if (cont % 100 != 0 or cont == 0) and cont != 572:
            usernames[aux] = usernames[aux] + str(item.name).replace(" ", "")[0:13] + ","
            cont += 1
        elif cont % 100 == 0:
            # Coloca no foramto correto 100 nomes de deputados para colocar na url da requisição
            usernames[aux] = usernames[aux][:-1]
            usernames[aux] = unidecode(usernames[aux]).replace(".", "").replace("'","").replace("-","")
            
            #Incrementa para poder iniciar mais 100 nomes já adicionando os deputados nas posições x00, preparando os pareametros da próxima requisição
            aux += 1
            usernames[aux] = usernames[aux] + str(item.name).replace(" ", "")[0:13] + ","
            cont += 1
        
        #Caso do último deputado no DB (tirando os de teste)
        else:
            usernames[aux] = usernames[aux] + str(item.name).replace(" ", "")[0:13] + ","
            usernames[aux] = usernames[aux][:-1]
            usernames[aux] = unidecode(usernames[aux]).replace(".", "").replace("'","").replace("-","")
            break

    # Lista com todos os resultados de cada nome de deputado
    json_deputies_usernames = []

    # Adiciona o resultado (jsons) de cada requsição com seus devidos parâmetros na lista
    for usernames_100 in usernames:
        json_deputies_usernames.append(metodo_de_request(usernames_100))

    # Lista com os deputados que são verificados
    json_deputies_verified = []

    # Procura os perfis que são verificados
    for r_result in json_deputies_usernames:
        for username in r_result['data']:
            if username['verified'] is True:
                json_deputies_verified.append(username)


    # Retorma o JSON com os deputados que possuem perfis verificados no Twitter
    return jsonify(json_deputies_verified)

# Metodo que faz os requests pra API dos usernames do Twitter e retorna os resultados em JSON
def metodo_de_request(usernames):
    r = requests.get(f"https://api.twitter.com/2/users/by?{usernames}&user.fields=verified,url", headers=auth_header)
    return r.json()

# Rota que retorna infos de usernames especificos listados
@api.route('/user_lookup_by_username')
def user_lookup_by_username():

    # Parametros de busca:
    # usernames = "usernames=ANAMARIABRAGA,varien"
    usernames = "usernames="
    cont = 0
    deputies_verified = []

    for item in Deputy.objects:
        cont += 1

    print("TOTAL DEPUTADOS =", cont)

    cont = 0
    # Parametros de busca:
    # usernames = "usernames=ANAMARIABRAGA,varien"
    usernames = "usernames="
    cont = 0

    # Loop que preencherá o parâmetro de usernames da pesquisa, procurando se algum deputado é usuário do twitter (suporta até 100 usernames)
    for item in Deputy.objects:
        if cont < 100:
            usernames = usernames + str(item.name).replace(" ", "")[0:13] + ","
            cont += 1
        else: 
            usernames = usernames[:-1]
            break
    
    if(cont < 100):
        usernames = usernames[:-1]

    print("\n", cont, "\n")
        
    # Retira possiveis acentuações nos names
    usernames = unidecode(usernames).replace(".", "")

    r = requests.get(f"https://api.twitter.com/2/users/by?{usernames}&user.fields=verified,url", headers=auth_header) # POde ser que esteja faltando o '&' no final dessa url
    
    deputies_username_json = r.json()

    # Adiciona todos os perfis que são verificados(que existem ou não estão suspensos)
    for item_json in deputies_username_json['data']:
        if item_json['verified'] is True:
            temp_json = item_json
            deputies_verified.append(temp_json)

    return jsonify(deputies_verified)
    
    
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

#Atualiza o banco de dados do twitter
@api.route('/update_twitter_accounts')
def update_twitter_accounts():
    for item in Deputy.objects:

        #verificar se o edputado já tem seu twitter vinculado, se tiver, só passa pro próximo
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
            print("Essa request não tem uma response") 
            continue 

        deputy_twitter_json = r.json()

        #criar uma ctring para conseguir verificar se ele possue a chave data
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

# Rota que retorna até 10 tweets mais recentes do usuario indicado pelo seu id
@api.route('/update_tweets')
def update_tweets():
    
    # for item in Deputy.objects:
        
    #     if item.twitter_id:
    #         r = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets", headers=auth_header, params=params)

    #         if not r:
    #             continue
            
    #         last_10_tweets_json = r.json()


    user_id = 36679967 #ID da Ana Maria Braga
    # user_id = 2244994945

    params = get_params()

    r = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets", headers=auth_header, params=params)
    
    return r.json()

@api.route('/get_all_deputies')
def get_all_deputies():
    t = []
    for item in Deputy.objects:
        t.append(item.to_json())

    return jsonify(t)
