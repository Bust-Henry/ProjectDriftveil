from dotenv import load_dotenv
load_dotenv()
import os
import json
dirname = os.path.dirname(__file__)
import socket
import subprocess
import typing
import sys
from bitstring import BitArray
from dbconnector import DBConnector
from datetime import datetime
""" 
class byteParser():
    TYPE_BOOL = "bool"
    TYPE_INT = "int"
    TYPE_LONG = "long"
    TYPE_U_LONG = "ulong"
    TYPE_ARRAY_INT = "int[]"
    TYPE_DICT_INT_INT = "dict<int,int>"
    TYPE_DICT_INT_BOOL = "dict<int,bool>"
    TYPE_STRING = "string"

    def get_parse_func(self, type:str):
        if type == self.TYPE_BOOL:
            return self.parseBool
        if type == self.TYPE_INT:
            return self.parseInt
        else:
            return None

    def parseBool(self,bytes):
        if bytes == b'':
            return None
        if bytes == b'\x01':
            return True
        if bytes == b'\x00':
            return False

    def parseInt(self,bytes)->int:
        print(bytes)
        return int.from_bytes(bytes, 'little',signed =False) """

def readString(file:typing.BinaryIO):
    len = int.from_bytes(file.read(1),byteorder=sys.byteorder)
    return file.read(len)

def read4Array(file:typing.BinaryIO):
    id = file.read(2)
    lenByte = BitArray(file.read(1))
    if lenByte.bin == '':
        return False
    # cut away leading 0b and the 4 first bit
    len = int(lenByte.bin[4:],2) * 4
    return file.read(len)

def read5Array(file:typing.BinaryIO):
    id = file.read(2)
    lenByte = BitArray(file.read(1))
    if lenByte.bin == '':
        return False
    # cut away leading 0b and the 4 first bit
    len = int(lenByte.bin[4:],2) * 5
    return file.read(len)

def read8Array(file:typing.BinaryIO):
    id = file.read(2)
    lenByte = BitArray(file.read(1))
    if lenByte.bin == '':
        return False
    # cut away leading 0b and the 4 first bit
    len = int(lenByte.bin[4:],2) * 8
    return file.read(len)

def getFormat(str:str):
    """This function returns the right parse function for the given format

    Args:
        str (str): the format of the upcoming bytes (exp. '4X')
    Returns:
        function: the function to call to parse the given format
    """
    if str == "4X":
        return read4Array
    if str == "5X":
        return read5Array
    if str == "8X":
        return read8Array
    if str == "S":
        return readString
    if str == "D":
        return readString
     

def getBoxData():
    """this function takes a bytefile (exp. save file from pokemon home) and formats it after the configured byteMapping (see byteMapping.json)
    """
    bytefile = os.path.join(dirname, os.environ.get("decodedbytefile"))
    jsonfile = os.path.join(dirname, os.environ.get("byteMapping"))
    # open byte mapping and reading bytes from file:
    byteMapping:dict = json.load(open(jsonfile, "r"))
    # splitting bytestream in chunks equal to the calculated chunk of bytes that describe one pokemon
    filedata = byteMapping.pop("filedata")
    with open(bytefile, "rb") as bytefile:
        # skip the beginning of the file, because it doesnt contain pokemon data
        currentbyte = bytefile.read(filedata["unknown"])
        len = int.from_bytes(bytefile.read(filedata["len"]), "little", signed=False)
        currentbyte = bytefile.read(filedata["skip"])
        pokemon = []
        print("no. of pokemon in this save file:", len)
        i = 1
        while i <= len:
            currentpokemon = {}
            for category in byteMapping.values():
                for key, value in category.items():
                    if isinstance(value, str):
                        #value is a string so we have to determine the reading method
                        currentbyte = getFormat(value)(bytefile)
                        if currentbyte == False:
                            print("early canceled at pokemon no." , i, ". something is wrong with the length of the stream")
                            return pokemon
                    else:
                        currentbyte = bytefile.read(value)
                    if currentbyte == b'\xFF':
                        # early cancel, incase something went wrong with the length
                        print("early canceled at pokemon no." , i, ". something is wrong with the length of the stream")
                        return pokemon
                    currentpokemon[key] = currentbyte
            pokemon.append(currentpokemon)
            i += 1
        print("no extraced:", i)
        return pokemon


""" def translateBoxData(pokemon:list):
    jsonfile = os.path.join(dirname, os.environ.get("typeMapping"))
    typeMapping:dict = json.load(open(jsonfile, "r"))
    for mon in pokemon:
        for category in typeMapping.values():
            for key, value in mon.items():
                print(key,value)
                if key in category:
                    parsefunc = byteParser().get_parse_func(category[key])
                    if parsefunc == None:
                        continue
                    else:
                        mon[key] = parsefunc(value)
                else:
                    print("no type mapping available for: ", key)
    return pokemon """

def decryptFile():
    bytefile = os.path.join(dirname, os.environ.get("bytefile"))
    decodedbytefile = os.path.join(dirname, os.environ.get("decodedbytefile"))
    decryptExe = os.path.join(dirname, os.environ.get("decryptExe"))
    subprocess.call(f"{decryptExe} {bytefile} {decodedbytefile}")
    #adding a flag to the end of the file for better iterating
    with open(decodedbytefile, "ab") as file:
        file.write(b'\xFF')

def receive(dbcon:DBConnector, port:int=5050):
    """binds to the given port to accept save data from pokemon home. This function is blocking and can only be manually shut down.
    This function is designed to run on its own, because it continously binds to the port and accepts new clients.

    Args:
        port (int, optional): port that the socket accepts data from. Defaults to 5050.
    Calls:
        homeConnector.getBoxData
    """
    filepath = os.path.join(dirname, os.environ.get("bytefile"))
    #Create a socket object.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Bind the socket.
    sock.bind( ("", 5050) )
    #Start listening.
    sock.listen()
    try:
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
                #append stream
                stream+=received
            starttime = datetime.now()
            with open(filepath, "wb") as bytefile:
                bytefile.write(stream)
            decryptFile()
            dbcon.updateDatabase(getBoxData())
            print("time for this action:", (datetime.now() - starttime).total_seconds())
    except KeyboardInterrupt:
        pass
        
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), os.environ.get("dbpath"))
    con = DBConnector(path)
    import threading
    thread = threading.Thread(target=receive, args=(con,5050), daemon=True)
    thread.start()
    input('Waiting for data, press return to terminate server...')