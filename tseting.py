# Import socket module 
import socket             

# Create a socket object 
s = socket.socket()         

# Define the port on which you want to connect 
port = 8000                

# connect to the server on local computer 
s.connect(('192.168.0.160', port)) 

# receive data from the server and decoding to get the string.
while 1:
    server_msg=s.recv(1024).decode()
    if "INPUT" in server_msg:
        msg=input(server_msg)
        if not msg: msg="error"
        s.send(msg.encode())
    
    else:
        print(server_msg)
    if msg.lower()=="exit":
        print("exiting program")
        break

# close the connection 
s.close()
