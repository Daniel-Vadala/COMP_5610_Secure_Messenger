import socket
import AESEncryption
import diffiehelman
import pickle

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

bob = 0
alice = diffiehelman.DiffieHellman()

port = 9999
buffer = 1024
# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    msg = clientsocket.recv(buffer)
    msg = pickle.loads(msg)
    print ("received message")
   # if (len(str(msg)) == 540): #the diffie hellman piece
    print("got into the if statement")
    bob = msg
    temp = pickle.dumps(alice.publicKey)
    clientsocket.send(temp)
    alice.genKey(bob)
    key = alice.getKey()
    key2 = clientsocket.recv(buffer)
    key2 = pickle.loads(key2)
    print ("key2 done")
    temp = pickle.dumps(key)
    clientsocket.send(temp)
    if(key != key2):
        clientsocket.close()
        raise SystemExit(0)

    #msg = 'Thank you for connecting' + "\r\n"
    msg = clientsocket.recv(buffer)
    msg = pickle.loads(msg)
    print(msg)
    msg = "return message"
    temp = AESEncryption.encryptText(key, msg)
    clientsocket.send(temp)
    clientsocket.close()