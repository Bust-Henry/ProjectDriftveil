import os
import json
import dexScraper
from dbconnector import DBConnector, PokemonElement
import imageRecognition
from blueStackController import BlueStackController
import argparse
import time
from datetime import datetime

class reading():
    def __init__(self, nr, lvl, hp) -> None:
        self.nr = nr
        self.lvl = lvl
        self.hp = hp
    
    def compare(self, reading):
        if self.compareNr(reading) and self.compareLvl(reading) and self.hp == reading.hp:
            return True
        return False

    def compareNr(self, reading):
        if self.nr == reading.nr:
            return True
        return False
    
    def compareLvl(self, reading):
        if self.lvl == reading.lvl:
            return True
        return False
    
    def toString(self):
        return f"nr: %s, lvl: %s, hp: %s" %(self.nr, self.lvl, self.hp)

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

def registerBoxes(bluestackcontroller:BlueStackController, con:DBConnector):
    starttime = datetime.now()
    lastPokemon = reading(0,0,0)
    currentPokemon = reading(0,0,1)
    pokemonToRegister = []
    while True:
        pokemon = readPokemon(bluestackcontroller)
        currentPokemon = reading(pokemon[0], pokemon[1], pokemon[2])
        time.sleep(0.4)
        bluestackcontroller.nextPokemon()
        time.sleep(0.4)
        if not currentPokemon.compare(lastPokemon):
            pokemonToRegister.append(currentPokemon)
            print(currentPokemon.toString())
            lastPokemon = currentPokemon
            continue
        else:
            break
    for pokemon in pokemonToRegister:
        con.registerPokemon(pokemon.nr)
    bluestackcontroller.clearScreenshots()
    print("seconds:", (datetime.now() - starttime).total_seconds())

def readPokemon(bluestackcontroller:BlueStackController, calibrate = False):
    bluestackcontroller.setForeGround()
    bluestackcontroller.screenshot()
    result = bluestackcontroller.renameScreenshot("screenshot.png")
    if not result:
        print("renaming screenshot timed out")
        exit()
    data = imageRecognition.readBluestacks(calibrate)
    bluestackcontroller.deleteScreenshot()
    return data

if __name__=="__main__":
    # --------------------------argument parser options------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--rebuild', action='store_true', help="rebuild the pokemon database")
    parser.add_argument('-c','--calibrate', action='store_true', help="calibrate the areas of text")
    parser.add_argument('--clearRegistered', action='store_true', help="clears all registered pokemon")
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
    con = DBConnector(os.environ.get("dbpath"))

    # if script startet with --rebuild flag, the database will be rebuilt.
    if args.rebuild:
        rebuild_database()
    if args.clearRegistered:
        con.clearRegisteredPokemon()
        print("registered pokemon cleared")
        exit()
    controller = BlueStackController()
    if args.calibrate:
        readPokemon(controller,calibrate=True)
    else:
        registerBoxes(controller, con)
