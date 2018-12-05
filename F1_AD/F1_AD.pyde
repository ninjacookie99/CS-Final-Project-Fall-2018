add_library('minim')
import os,random,time
path = os.getcwd()
player = Minim(this)

class Vehicle:
    def __init__(self,x,y,r,g,img,w,h,F):
        self.x=x
        self.y=y
        self.r=r
        self.g=g
        self.vx=0
        self.vy=0
        self.w=w
        self.h=h
        self.F=F
        self.f=0
        self.img= loadImage(path+"/Images/"+img)
        self.dir = 1
  
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
    
        if self.dir > 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
    
class f1Car(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False,DOWN:False}
        
    def update(self):
        if self.keyHandler[RIGHT]:
            self.vx = 15
            self.dir = 1
        elif self.keyHandler[UP]:
            self.vy = -3
            self.dir = 1
        elif self.keyHandler[DOWN]:
            self.vy = 3
            self.dir = 1
            
        self.x += self.vx
        self.y += self.vy
        
        if self.x > game.w/2:
            game.x += self.vx

class Ambulance(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -6

class Police(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -4.5
 
class Taxi(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -3

class Viper(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -5

class Coin:
    def __init__(self,x1,y1,r1,img,w1,h1,F):
        self.x1 = x1
        self.y1 = y1
        self.r1 = r1
        self.w1 = w1
        self.h1 = h1
        self.F = F
        self.f = 0
        self.img = loadImage(path+"/Images"+img)

# class Explosion:
    
#class PowerUp:
    
class Game:
    def __init__(self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.x=0
        self.pause = False
        #images
        self.win_img = loadImage(path+"/Images/win.jpg")
        self.lose_img = loadImage(path+"/Images/gameover.png")
        self.f1Car = f1Car(50,665,80,self.g,"f1Car.png",110,80,7)
        # self.police = Police(50,665,80,self.g,"police.png",110,80,1)
        # self.ambulance = Ambulance(50,665,80,self.g,"ambulance.png",110,80,1)
        # self.taxi = Taxi(50,665,80,self.g,"taxi.png",110,80,1)
        # self.viper = Viper(50,665,80,self.g,"viper.png",110,80,1)
        # self.truck = Truck(50,665,80,self.g,"truck.png",110,80,1)
        self.bgImgs=[]
        for i in range(6,0,-1):
            self.bgImgs.append(loadImage(path+"/Images/layer"+str(i)+".png"))
        self.enemies=[]
        
        #sounds
        self.pauseSound = player.loadFile(path+"/Effects/pause.mp3")
        self.music = player.loadFile(path+"/Effects/background.mp3")
        self.music.play()
        self.winSound = player.loadFile(path+"/Effects/win.mp3")
        self.loseSound = player.loadFile(path+"/Effects/lose.mp3")
        self.f1Sound = player.loadFile(path+"/Effects/formula1.mp3")
        self.taxiSound = player.loadFile(path+"/Effects/taxi.mp3")
        self.ambulanceSound = player.loadFile(path+"/Effects/ambulance.mp3")
        self.policeSound = player.loadFile(path+"/Effects/police.mp3")
            
    def display(self):
        cnt = 6
        for img in self.bgImgs:
            x = (game.x//cnt)%game.w
            image(img,0-x,0)
            image(img,self.w-x,0)
            cnt-=1
            
        self.f1Car.display()
    
game = Game(1440,900,500)

def setup():
    size(game.w,game.h)
    background(0)
    
def draw():
    stroke(255)
    line(0,game.g,1440,game.g)
    game.display()

def keyPressed():
    if keyCode == LEFT:
        game.f1Car.keyHandler[LEFT]=True
    elif keyCode == RIGHT:
        game.f1Car.keyHandler[RIGHT]=True
        game.f1Sound.rewind()
        game.f1Sound.play()
    elif keyCode == UP:
        game.f1Car.keyHandler[UP]=True
    elif keyCode == DOWN:
        game.f1Car.keyHandler[DOWN]=True
    elif keyCode == 80:
        game.pause = not game.pause
        game.pauseSound.rewind()
        game.pauseSound.play()
        if game.pause == True:
            game.music.pause()
        else:
            game.music.play()

def keyReleased():  
    if keyCode == UP:
        game.f1Car.keyHandler[UP]=False
    elif keyCode == DOWN:
        game.f1Car.keyHandler[DOWN]=False
    elif keyCode == LEFT:
        game.f1Car.keyHandler[LEFT]=False
    elif keyCode == RIGHT:
        game.f1Car.keyHandler[RIGHT]=False
        
        
