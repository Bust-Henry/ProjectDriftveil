from dotenv import load_dotenv
load_dotenv()
import os
import json
filepath = os.path.join(os.path.dirname(__file__), os.environ["byteMapping"])
import socket

def getBoxData(bytestream:bytearray):
    """this function takes a bytestream (exp. save file from pokemon home) and formats it after the configured byteMapping (see byteMapping.json)

    Args:
        bytestream (bytearray): a bytestream containing save data from one or multiple pokemon ()
    """
    # open byte mapping and reading bytes from file:
    byteMapping = json.load(open(filepath, "r"))
    # splitting bytestream in chunks equal to the calculated chunk of bytes that describe one pokemon
    elementsize = byteMapping["size"]
    bytechain = []
    bytePokemon = []
    i = 0
    for byte in bytestream:
        if i >= elementsize:
            bytePokemon.append(bytechain)
            bytechain = []
            i = 0
        bytechain.append(byte)
        i += 1
    # split up bytechunks into valuable data (byteMapping contains keys and start and stop bytes for those values)
    # example: the value shinyFlag is in byte 10 unitl 12
    pokemon = []
    for element in bytePokemon:
        mapping:dict = byteMapping["data"]
        pokemondict = {}
        for key, value in mapping.items():
            pokemondict[key] = element[value[0]:value[1]]
        pokemon.append(pokemondict)
    print(pokemon)

def receive(port:int=5050):
    """binds to the given port to accept save data from pokemon home. This function is blocking and can only be manually shut down.
    This function is designed to run on its own, because it continously binds to the port and accepts new clients.

    Args:
        port (int, optional): port that the socket accepts data from. Defaults to 5050.
    Calls:
        homeConnector.getBoxData
    """    
    print("waiting for data")
    #Create a socket object.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Bind the socket.
    sock.bind( ("", 5050) )
    #Start listening.
    sock.listen()
    while True:
        #Accept client.
        client, addr = sock.accept()
        #Receive all the bytes and write them into the file.
        stream = b''
        while True:
            received = client.recv(5)
            #Stop receiving.
            if received == b'':
                break
            #Write bytes into the file.
            stream+=received
        getBoxData(stream)


if __name__ == "__main__":
    receive()
    rec