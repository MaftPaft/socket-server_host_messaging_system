import pygame as pg
import socket
import threading
from random import randint

haddr=('192.168.0.150',5050)
addr=[haddr[0]]
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(haddr)

player_data={}
def client_handler():
    global client, player_data
    while True:
        data=client.recv(64).decode()
        if data:
            if "_" in data:
                add=data.split("_")[0]
                if len(add) == 5:
                    player_data[add]=data.split("_")[1]

def send(msg):
    message = msg.encode()
    msg_length = len(message)
    send_length = str(msg_length).encode()
    send_length += b' ' * (64-len(send_length))
    client.send(send_length)
    client.send(message)

def main():
    global client, player_data
    w,h=800,600
    win=pg.display.set_mode((w,h))
    fps=120
    x=randint(5,w)
    y=randint(5,h)
    run=True
    clock=pg.time.Clock()
    while run:
        mx,my=pg.mouse.get_pos()
        mp=pg.mouse.get_pressed()
        for i in pg.event.get():
            if i.type == pg.QUIT:
                send("!DISCONNECT")
                run=False
        win.fill((0,0,0))
        if mp[0]:
            x,y=mx,my
        pos=f"x:{int(x)},y:{int(y)}"
        if player_data:
            for p in player_data.items():
                px,py=p[1].replace("x:","").replace("y:","").split(",")
                pg.draw.circle(win,(255,0,0),(int(px),int(py)),10,1)
        pg.draw.circle(win,(0,255,0),(x,y),10,1)
        send(pos)
        pg.display.update()
        clock.tick(fps)

threading.Thread(target=client_handler).start()
threading.Thread(target=main).start()
