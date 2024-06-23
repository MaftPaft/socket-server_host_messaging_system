import socket
import threading

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
server.bind(ADDR)
clients=[]
def client_handler(conn,addr):
    global clients
    run=True
    while run:
        msg=conn.recv(64).decode('utf-8')
        if msg:
            if msg == "!DISCONNECT":
                print(f"{addr} left the server")
                run=False
            else:
                sender=f"[{addr}]: {msg}"
                for client in clients:
                    client[0].send(sender.encode())
    conn.close()

def start():
    global clients
    server.listen()
    print(f"{ADDR} LISTENING")
    while True:
        conn,addr=server.accept()
        threading.Thread(target=client_handler,args=(conn,addr)).start()
        clients.append((conn,addr))
start()
