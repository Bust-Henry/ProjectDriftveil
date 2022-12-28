import requests
import os
from dotenv import load_dotenv
load_dotenv()

def getPokemon(number):
    response = requests.get(os.environ.get("api") + "pokemon/" + str(number))
    if response.status_code == 200:
        return response.json()
    return None

def getAllPokemon(startAt:int=1):
    i = startAt
    pokemonList = []
    while True:
        pokemon = getPokemon(i)
        if pokemon is not None:
            pokemonList.append(pokemon)
            i+=1
        else:
            break
    return pokemonList

if __name__=="__main__": 
    os.environ["api"] = "https://pokeapi.co/api/v2/"
    print(getAllPokemon())