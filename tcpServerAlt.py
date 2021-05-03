#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket
from threading import Thread
import pickle
import diffiehelman
from AESEncryption import encryptText, decryptText

clients = {}
addresses = {}
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
HOST = local_ip
PORT = 9999
buffer = 1024
bob = 0
alice = diffiehelman.DiffieHellman()

ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        msg = client.recv(buffer)
        msg = pickle.loads(msg)
        bob = msg
        temp = pickle.dumps(alice.publicKey)
        client.send(temp)
        alice.genKey(bob)
        key = alice.getKey()

        addresses[client.getsockname()] = {"Address": client_address, "Key": key, "Client": client } 
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    print("started handler")
    while True:
        print("made it to while loop")
        msg = client.recv(buffer)
        if msg == bytearray("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

        elif msg:
            print(msg)
            message = pickle.loads(msg)
            address = client.getsockname()
            decryptedMessage = decryptText(addresses[address]["Key"], message["Message"], message["Nonce"])
            if(decryptedMessage):
                broadcast(decryptedMessage, message["Username"])


def broadcast(msg, userName = "Unkown"):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for key in addresses.keys():
        encryptedMessage, nonce = encryptText(addresses[key]["Key"], msg)
        finalMessage = {"Message": encryptedMessage, "Nonce": nonce, "Username": userName}
        encodedMessage = pickle.dumps(finalMessage)
        addresses[key]["Client"].send(encodedMessage)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
