import socket

#Create a socket object.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
#Connect to the server.
try:
    sock.connect(("192.168.178.100", 5050))
    with open("/sdcard/Android/data/jp.pokemon.pokemonhome/files/utsudon/34be958a921e43d813a2075297d8e862", "rb") as file:
        sock.sendfile(file)
except TimeoutError:
    print("socket connection timed out!")
except FileNotFoundError:
    print("savefile was not found!")
except ConnectionRefusedError:
    print("connection was refused! Make sure the server is running!")

sock.close()
print("done!")