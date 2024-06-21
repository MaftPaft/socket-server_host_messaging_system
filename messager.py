import socket
import threading

class server_host:
    def __init__(self,port,host=socket.gethostbyname(socket.gethostname()),HEADER=64,FORMAT='utf-8'):
        self.header=HEADER
        self.format=FORMAT
        self.ADDR=(host,port)
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients=[]
    def bind(self):
        self.server.bind(self.ADDR)
    def handle_clients(self,conn,addr,disconnect_msg='!DISCONNECT'):
        connection=True
        while connection:
            msg_length = conn.recv(self.HEADER).decode(self.format)
            if msg_length:
                msg_length=int(msg_length)
                msg = conn.recv(msg_length).decode(self.format)
                if msg == disconnect_msg:
                    dsmg=f"{addr} left the server"
                    print(dsmg)
                    for i in range(len(self.clients)):
                        if self.clients[i][1] != addr:
                            self.clients[i][0].send(dsmg.encode(self.format))
                    self.clients.remove((conn,addr))
                    connection = False
                else:
                    print(f"[{addr}] {msg}")
                    for i in range(len(self.clients)):
                        if self.clients[i][1] != addr:
                            self.clients[i][0].send(msg.encode())
        conn.close()
    def start(self):
        self.server.listen()
        print(f"[LISTENING] server is listening {self.ADDR[0]}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client,args=(conn,addr))
            thread.start()
            print(f"[AVTIVE CONNECTIOSN] {threading.activeCount() -1}")
            self.clients.append((conn,addr))
            
class client_socket:
    def __init__(self,ADDR,HEADER=64,FORMAT='utf-8'):
        self.ADDR=ADDR
        self.header=HEADER
        self.format=FORMAT
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    def connect(self):
        try:
            self.client.connect(self.ADDR)
        except:
            raise ValueError("Server is offline (Did you use the server_host? Try disabling firewall*)")
    def send(self,msg):
        message=msg.encode(self.format)
        msg_length=len(message)
        send_length=str(msg_length).encode(self.format)
        send_length+=b' ' * (self.header-len(send_length))
        self.client.send(send_length)
        self.client.send(msg)
    def read(self):
        msg=self.client.recv(self.header).decode(self.format)
        if msg:
            print(msg)
        
