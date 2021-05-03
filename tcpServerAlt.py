#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket
from threading import Thread
import pickle
import diffiehelman

clients = {}
addresses = {}
HOST = socket.gethostname()
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
        key2 = client.recv(buffer)
        key2 = pickle.loads(key2)
        print("key2 done")
        temp = pickle.dumps(key)
        client.send(temp)
        if (key != key2):
            client.close()
            raise SystemExit(0)
        #client.send(bytes("Greetings from the cave!" +
                          #"Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    print("started handler")
    name = client.recv(buffer)#.decode("utf8")
    broadcast(name,)
    #welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    #client.send(bytes(welcome, "utf8"))
   # msg = "%s has joined the chat!" % name
    print("first broadcast")
    #broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(buffer)
        print("made it to while loop")
        if msg == bytearray("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

        elif msg:
            print("infinite broadcast")
            broadcast(msg)


def broadcast(msg ):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send( msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
