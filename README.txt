Secure Messenger

Dylan Palmer
Daniel Vadala

Install commands:
pip install pycryptodomex
or
easy_install pycryptodomex

https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

run commands
Server code: python tcpServer.py
Client UI Code: python main.py

Description:
We created a secure messenger app using AES encryption scheme and Diffie Helman Key Exchanges.  Using Python’s socket library along with AES and Diffie Hellman libraries,
our application connects clients securely to a single server, sending encrypted messages among the clients.  We also utilized python’s built in tkinter library for UI and
pickle library for data conversion to bytes to send over the web.

Instructions:
First start up the server code, once that is started run the main files to open the log in screen.  Use the new log in entries to create a new log in account, and a new
Client will start with a messagenger UI. It will default look for the local server running and connect to it.  Next you can use the same log in UI to create another user
which will open a second client.  Once the two clients are open you can use the UI to message between the two clients.  If the server code is running on a reachable server,
you can specify the IP of the server you are trying to connect to.