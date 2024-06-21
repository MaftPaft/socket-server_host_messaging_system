import pygame as pg
import socket
import threading

class multiplayer_host:
    def __init__(self,port,host=socket.gethostbyname(socket.gethostname())):
        self.H=64
        self.F='utf-8'
        self.addr=(host,port)
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients=[]
    def bind(self):
        self.server.bind(self.addr)
    def handling_clients(self,conn,addr):
        run=True
        while run:
            msg=conn.recv(self.H).decode(self.F)
            if msg:
                if msg == "!DISCONNECT":
                    self.clients.remove((conn,addr))
                    run=False
                elif "x: " in msg and "y: " in msg:
                    for c in range(len(self.clients)):
                        p=msg.replace("x: ","").replace("y: ","").split(",")
                        send=f"{addr[1]}_x: {p[0]}, y: {p[1]}"
                        self.clients[c][0].send(send.encode(self.F))
        conn.close()
    def start(self):
        self.server.listen()
        while True:
            conn,addr=self.server.accept()
            threading.Thread(target=self.handling_clients,args=(conn,addr)).start()
            self.clients.append((conn,addr))

server=multiplayer_host(1234)
server.bind()
server.start()
