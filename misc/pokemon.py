import requests
import os
from dotenv import load_dotenv
load_dotenv()

class Pokemon:
    number = 0 # the pokemon number
    name = "" # the pokemon name
    games = [] # contains all the games where the pokemon can be caught (maybe non existent for newer pokemon)
    data = None # contains all the data a pokemon can have (fetched from the pokemon api)

    def __init__(self, number) -> None:
        self.number = number
        self.data = Pokemon.fetchdata(number)
        if self.data is not None:
            self.name = self.data["species"]["name"]
            for indecies in self.data["game_indices"]:
                self.games.append(indecies["version"]["name"])
        
    def fetchdata(number:int)->dict:
        try:
            api = os.environ.get("api")
            response = requests.get(api + f"pokemon/{number}", timeout=5)
            return response.json()
        except:
            return None

    def getPokemon(number):
        response = requests.get(os.environ.get("api") + "pokemon/{number}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None

    def getAllPokemon(startAt:int=1):
        i = startAt
        pokemonList = []
        while True:
            pokemon = Pokemon.getPokemon(i)
            if pokemon is not None:
                pokemonList.append(pokemon)
                i+=1
            else:
                break
        return pokemonList

if __name__ == "__main__":
    pokemon = Pokemon(200)
    print(pokemon.name)