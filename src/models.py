from mongoengine import *

class Deputy(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    photo_url = StringField()
    initial_legislature_id = IntField(required=True)
    final_legislature_id = IntField()
    initial_legislature_year = IntField(required=True)
    final_legislature_year = IntField()
    last_activity_date = DateTimeField()
    full_name = StringField()
    sex = StringField()
    email = StringField()
    birth_date = DateTimeField()
    death_date = DateTimeField()
    federative_unity = StringField()
    party = StringField()
    instagram_username = StringField()
    twitter_username = StringField()
    facebook_username = StringField()

    def to_json(self, context):
        return{
            'id':context.id,
            'name':context.name,
            'photo_url':context.photo_url,
            'initial_legislature_id':context.initial_legislature_id,
            'final_legislature_id':context.final_legislature_id,
            'initial_legislature_year':context.initial_legislature_year,
            'final_legislature_year':context.final_legislature_year,
            'last_activity_date':context.last_activity_date,
            'full_name':context.full_name,
            'sex':context.sex,
            'email':context.email,
            'birth_date':context.birth_date,
            'death_date':context.death_date,
            'federative_unity':context.federative_unity,
            'party':context.party,
            'instagram_username':context.instagram_username,
            'twitter_username':context.twitter_username,
            'facebook_username':context.facebook_username
        }

# class News(Document):
#     id = IntField(primary_key=True)
#     deputy_id = IntField()
#     link = StringField()
#     photo = StringField()
#     title = StringField()
#     abstract = StringField()
#     deputy_name = StringField()
#     update_date = DateTimeField()
#     source = StringField()

class DBTest(Document):
    message = StringField()

class Tweet(Document):
    tweet_id = IntField(primary_key=True)
    deputy_id = IntField()
    name = StringField()
    twitter_username = StringField()
    date = DateTimeField()

    def to_json(self, context):
        return {
            'tweet_id':context.tweet_id,
            'deputy_id':context.deputy_id,
            'name':context.name,
            'twitter_username':context.twitter_username,
            'date':context.date
        }
