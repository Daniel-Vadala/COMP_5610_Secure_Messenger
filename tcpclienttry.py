import socket
import AESEncryption
import diffiehelman
import pickle

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

bob = diffiehelman.DiffieHellman()
print(bob.publicKey)
alice = 0

port = 9999
buffer = 1024
file = 'data.txt'
#myFile = open(file, 'rb')
# connection to hostname on the port.
s.connect((host, port))
msg = pickle.dumps(bob.publicKey)
s.send(msg)
print ("line 1")
alice = s.recv(buffer)
print (alice)
alice = pickle.loads(alice)
print (alice)
bob.genKey(alice)
key = bob.getKey()
print(key)
temp = pickle.dumps(key) #can't pickle and send in same line
print("line 5")
s.send(temp)
print("line 6")
key2 = s.recv(buffer)
print("raw key2:", key2)
key2 = pickle.loads(key2)
print("key1:", key, "key2:", key2)
if (key != key2):
    print("system error")
    s.close()
    raise SystemExit(0)
print("before encryption")
msg = AESEncryption.encryptFile(key, file) #single encryted file send
temp = pickle.dumps(msg)
s.send(temp)
print("after encryption")
msg = s.recv(buffer)
msg = pickle.loads(msg)
s.close()
print(msg)