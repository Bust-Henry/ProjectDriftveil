import os
import json
import dexScraper
from dbconnector import DBConnector, PokemonElement
import imageRecognition
from blueStackController import BlueStackController
import argparse

def loadConfig(path):
    with open(path, "r") as jsonfile:
        return json.load(jsonfile)

def rebuild_database():
    print("rebuilding database, this might take a while")
    db = DBConnector(os.environ.get("dbpath"))
    db.createDB()
    pokemonList = dexScraper.getAllPokemon()
    for pokemon in pokemonList:
        db.add(PokemonElement(pokemon["id"], pokemon["species"]["name"], 0, 0))
    print("done")

if __name__=="__main__":
    # --------------------------argument parser options------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--rebuild', action='store_true', help="rebuild the pokemon database")
    parser.add_argument('-c','--calibrate', action='store_true', help="calibrate the areas of text")
    args = parser.parse_args()

    # --------------------------environment variables------------------------
    # setting environment variables
    os.environ['config'] = os.path.join(os.path.dirname(__file__), "data", "config.json")
    # loading config file
    config = loadConfig(os.environ.get("config"))
    # put every element in an environment variable
    for item in config.items():
        os.environ[item[0]] = item[1]
    
    # ------------------ Start Script -------------------

    # if script startet with --rebuild flag, the database will be rebuilt.
    if args.rebuild:
        rebuild_database()

    controller = BlueStackController()
    controller.setForeGround()
    controller.screenshot()
    import time
    time.sleep(1)
    controller.renameScreenshot("screenshot.png")
    print(imageRecognition.readBluestacks())
    controller.deleteScreenshot()
