import os
import json
import dexScraper
from dbconnector import DBConnector, PokemonElement
import imageRecognition
def loadConfig(path):
    with open(path, "r") as jsonfile:
        return json.load(jsonfile)

if __name__=="__main__":
    # setting environment variables
    os.environ['config'] = os.path.join(os.path.dirname(__file__), "data", "config.json")
    # loading config file
    config = loadConfig(os.environ.get("config"))
    # put every element in an environment variable
    for item in config.items():
        os.environ[item[0]] = item[1]
    
    # ------------------ Start Script -------------------
    """
    db = DBConnector(os.environ.get("dbpath"))
    db.createDB()
    #print(dexScraper.getHTML(os.environ.get("dexlink")))
    pokemonList = dexScraper.getAllPokemon()
    for pokemon in pokemonList:
        db.add(PokemonElement(pokemon["id"], pokemon["species"]["name"], 0, 0))
    print("done")"""
    print(imageRecognition.readPokemonNumber())