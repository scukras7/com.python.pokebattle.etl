import requests
import sys
sys.path.append('../services')
from pymongo import MongoClient
from EnvReaderService import EnvReaderService

getPokemonInfo          = True
getPokemonStats         = True
getPokemonLocationAreas = True
getEncounterMethod      = True
getGameVersion          = True
getMove                 = True

reader = EnvReaderService('production')

MONGO_URL = 'mongodb://' + \
    reader.vars()['MONGO_USER'] + ':' + \
    reader.vars()['MONGO_PASSWD'] + '@' + \
    reader.vars()['MONGO_HOST'] + ':' + \
    reader.vars()['MONGO_PORT'] + '/?authSource=' + \
    reader.vars()['MONGO_AUTHDB']

###############################################################################
###############################################################################
###############################################################################
# main

client = MongoClient(MONGO_URL)
db = client[reader.vars()['MONGO_DB']]

if getPokemonInfo:
    res = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=151')
    pokemon_base_list = res.json()['results']

    pokemon_info_list = []
    for pokemon_base in pokemon_base_list:
        print(pokemon_base['url'])
        res = requests.get(pokemon_base['url'])
        pokemon_info_list.append(res.json())

    db['pokemon'].insert_many(pokemon_info_list)

if getPokemonStats:

    stats = []
    
    res = requests.get('https://pokeapi.co/api/v2/stat/')
    stats_list = res.json()['results']

    for stat in stats_list:
        res = requests.get(stat['url'])
        stats.append(res.json())

    db['stats'].insert_many(stats)

if getPokemonLocationAreas:

    location_area_encounters = []

    location_area_encounters_urls = db['pokemon'].find({}, { '_id': 0, 'location_area_encounters': 1 })

    x =0
    for location_area_encounter_url in location_area_encounters_urls:
        url = location_area_encounter_url['location_area_encounters']
        print(url)
        res = requests.get(url)

        if len(res.json()) > 0:
            encounter = { 'id': url.split('/')[-2], 'encounters': [] }
            encounter['encounters'] = res.json()
            location_area_encounters.append(encounter)
    
    db['location_area_encounters'].insert_many(location_area_encounters)
     

if getEncounterMethod:

    encounter_methods = []

    res = requests.get('https://pokeapi.co/api/v2/encounter-method/?limit=200')
    encounter_methods_list = res.json()['results']

    for encounter_method in encounter_methods_list:
        url = encounter_method['url']
        print(url)
        res = requests.get(url)

        encounter_methods.append(res.json())

    db['encounter_methods'].insert_many(encounter_methods)

if getGameVersion:
    versions_list = requests.get('https://pokeapi.co/api/v2/version/?limit=100')
    
    versions = []

    for version in versions_list.json()['results']:
        version_url = version['url']

        print(version_url)
        res = requests.get(version_url)

        versions.append(res.json())

    db['game_versions'].insert_many(versions)

if getMove:

    moves_list = requests.get('https://pokeapi.co/api/v2/move?limit=1000')

    moves = []

    for i, move in enumerate(moves_list.json()['results']):
        i += 1
        name = move['name']

        url = 'https://pokeapi.co/api/v2/move/' + str(i)
        print(url)
        move_details = requests.get(url)

        try:
            moves.append(move_details.json())
        except:
            pass

    db['moves'].insert_many(moves)