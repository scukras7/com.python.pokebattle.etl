'''
Script to write sprite URLs from pokemondb.net to MongoDB
'''

import sys
sys.path.append('../services')
from pymongo import MongoClient
from EnvReaderService import EnvReaderService

#ENV_PROFILE = 'development'
ENV_PROFILE = 'production'
#ENV_PROFILE = 'uat'

reader = EnvReaderService(ENV_PROFILE)

reader.vars()['MONGO_PORT']

MONGO_URL = 'mongodb://' \
    + reader.vars()['MONGO_USER'] + ':' \
    + reader.vars()['MONGO_PASSWD'] + '@' \
    + reader.vars()['MONGO_HOST'] + ':' \
    + reader.vars()['MONGO_PORT'] + '/?authSource=' \
    + reader.vars()['MONGO_AUTHDB']

client = MongoClient(MONGO_URL)
db = client[reader.vars()['MONGO_DB']]

docs = db['pokemon'].find()


updates = []

for doc in docs:
    sprite_front_url = 'https://img.pokemondb.net/sprites/emerald/normal/' + doc['name'] + '.png'
    sprite_back_url = 'https://img.pokemondb.net/sprites/emerald/back-normal/' + doc['name'] + '.png'
    
    nDoc = doc['sprites']['pokemondb_front'] = sprite_front_url
    nDoc = doc['sprites']['pokemondb_back'] = sprite_back_url
    
    updates.append(nDoc)

print(updates)