'''
Script to write type_modifers csv table to MongoDB
'''

import sys
sys.path.append('../services')
from pymongo import MongoClient
from EnvReaderService import EnvReaderService

#ENV_PROFILE = 'development'
ENV_PROFILE = 'production'
#ENV_PROFILE = 'uat'

reader = EnvReaderService('development')

MONGO_URL = 'mongodb://' \
    + reader.vars()['MONGO_USER'] + ':' \
    + reader.vars()['MONGO_PASSWD'] + '@' \
    + reader.vars()['MONGO_HOST'] + ':' \
    + reader.vars()['MONGO_PORT'] + '/?authSource=' \
    + reader.vars()['MONGO_AUTHDB']

client = MongoClient(MONGO_URL)
db = client[reader.vars()['MONGO_DB']]

rows = []
documents = []

passthru = [ rows.append(row.replace('\n', '').split(',')) for row in open('../data/type_modifiers.csv', 'r') ]
headers = rows[0]

for i, row in enumerate(rows):
    if i > 0:
        doc = {}
        for j, header in enumerate(headers):
            if j == 0:
                doc['attackName'] = row[j]
            else:
                doc[header] = float(row[j])
        
        documents.append(doc)

db['type_modifiers'].insert_many(documents)