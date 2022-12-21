import socket

#Create a socket object.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to the server.
sock.connect(("192.168.178.100", 5050))

with open("C:/Users/Henry/Desktop/34be958a921e43d813a2075297d8e862", "rb") as file:
    sock.sendfile(file)

sock.close()