from messager import client_socket
import threading
SERVER='123.456.789'
PORT=1234
client = client_socket((SERVER,PORT))
client.connect()

run=True
def send_messages():
    global run
    msg=input('send: ')
    
    while run:
        if msg == "!DISCONNECT":
            client.send(msg)
            run=False
        else:
            client.send(msg)
            msg=input('send: ')

def read_messages():
    global run
    while run:
        msg=client.read()
        if msg:
            print("\n" + msg + "\nsend: ")

threading.Thread(target=send_messages).start()
threading.Thread(target=read_messages).start()
