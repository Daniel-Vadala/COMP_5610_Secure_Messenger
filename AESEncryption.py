import os, random, struct
from Cryptodome.Cipher import AES
import secrets


def encryptText(key, data, nonce=None, encode=False):
    if(encode):
        key = key.encode("utf-8")
    cipher = AES.new(key, AES.MODE_EAX)
    if(nonce == None):
        nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode("utf-8"))
    return ciphertext, nonce

def decryptText(key, data, nonce, encode=False):
    if(encode):
        key = key.encode("utf-8")
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(data)
    try:
        #cipher.verify(tag)
        return plaintext.decode("utf-8")
    except ValueError:
        print("Key incorrect or message corrupted")



def encryptFile(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize).rstrip(b"\0").decode("utf-8") 
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk.encode("utf-8") ))


def decryptFile(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def generateNewKey():
    return secrets.token_hex(16)