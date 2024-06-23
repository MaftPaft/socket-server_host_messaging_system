import pygame as pg
import socket
import threading
pg.init()
pg.mouse.set_visible(False)
class button:
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        # self.button_text=button_text
        self.is_clicked=False
        self.rect=pg.rect.Rect(self.x,self.y,self.width,self.height)
        self.mx,self.my=pg.mouse.get_pos()
        self.mp=pg.mouse.get_pressed()
    def update(self,window):
        self.mx,self.my=pg.mouse.get_pos()
        self.mp=pg.mouse.get_pressed()
        self.rect=pg.rect.Rect(self.x,self.y,self.width,self.height)
        
        
        if not self.rect.collidepoint(self.mx,self.my):
            pg.draw.rect(window,self.color,self.rect)
            pg.draw.polygon(window,(255,255,255),([self.mx,self.my],[self.mx,self.my+10],[self.mx,self.my],[self.mx+10,self.my+10]))
        else:
            color=[int(_/1.25) for _ in self.color] if not self.mp[0] else [int(_/1.5) for _ in self.color]
            pg.draw.rect(window,color,self.rect)
            pg.draw.polygon(window,(100,100,200),([self.mx,self.my],[self.mx,self.my+10],[self.mx,self.my],[self.mx+10,self.my+10]))
            
        pg.draw.rect(window,(255,255,255),self.rect,2,2)
    def on_click(self,action,*args):
        if self.rect.collidepoint(self.mx,self.my) and self.mp[0] and self.is_clicked == False:
            action(*args)
            self.is_clicked=True
        elif self.mp[0] == False:
            self.is_clicked=False
    def on_release(self,action,*args):
        
        if self.rect.collidepoint(self.mx,self.my) and self.mp[0] and self.is_clicked==False:
            self.is_clicked=True
        elif self.mp[0]==False and self.is_clicked==True and self.rect.collidepoint(self.mx,self.my):
            action(*args)
            self.is_clicked=False
        elif not self.rect.collidepoint(self.mx,self.my):
            self.is_clicked=False

class text_box:
    def __init__(self,x,y,width,height,base_color,txtcolor=(255,255,255)):
        self.x=x
        self.y=y
        self.width,self.height=width,height
        self.base_color=base_color
        self.txtcolor=txtcolor
        self.can_type=False
        self.current_text=''
    def update(self,window, exceptions=True):
        mx,my=pg.mouse.get_pos()
        mp=pg.mouse.get_pressed()
        rect=pg.rect.Rect(self.x,self.y,self.width,self.height)
        if rect.collidepoint(mx,my) and mp[0]:
            self.can_type=True
        elif mp[0] and exceptions:
            self.can_type=False
        pg.draw.rect(window,self.base_color,rect)
        txt=pg.font.SysFont("",self.height).render(self.current_text,False,self.txtcolor)
        pg.draw.rect(window,(0,0,0),pg.rect.Rect(self.x+txt.get_width(),self.y+self.height-(self.height/1.1),10,self.height/1.2))
        window.blit(txt,(self.x,self.y))
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('123.456.789.0', 1234))

log=[]
def reciever():
    global log,client
    while True:
        msg=client.recv(64).decode()
        if msg:
            log.append(msg)
def main():
    global log,client
    w,h=800,600
    win=pg.display.set_mode((w,h))
    b=button(w/1.25,h/1.25,100,50,(155,155,255))
    text=text_box(w/8,h/1.25,300,70,(155,155,255))
    console=pg.rect.Rect(10,50,w/2,h/2)

    def clickaction(msg:str):
        global log
        if msg:
            client.send(msg.encode())
            text.current_text=""

    fps=120
    clock=pg.time.Clock()
    run=True
    while run:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                client.send("!DISCONNECT".encode())
                run=False
            if i.type == pg.KEYDOWN and text.can_type:
                key=pg.key.name(i.key)
                if key == "backspace":
                    text.current_text=text.current_text[:-1]
                elif key == "space":
                    text.current_text+=" "
                else:
                    text.current_text+=pg.key.name(i.key)
        win.fill((100,0,100))

        pg.draw.rect(win,(0,0,0),console)
        for i in range(len(log)):
            font=pg.font.SysFont("",15).render(log[i],False,(255,255,255))
            x,y=console.x,console.y+i*15
            win.blit(font,(x,y))
        text.update(win,b.rect.collidepoint(b.mx,b.my) == False)
        b.update(win)
        b.on_release(clickaction,text.current_text)

        pg.display.update()
        clock.tick(fps)
    pg.quit()

threading.Thread(target=reciever).start()
threading.Thread(target=main).start()
