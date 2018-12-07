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
        self.velocity()
    
    def velocity(self): #<--- Need to modify velocity function to increase as game progresses
        self.x += self.vx
        self.y += self.vy
        
        if self.y+self.r < self.g:
            self.vy = 0
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0 
        
    def display(self):
        self.update()
        
        if isinstance (self, Police):
            self.f = (self.f+0.05)%self.F
        elif isinstance (self, Ambulance):
            self.f = (self.f+0.1)%self.F
        elif isinstance (self, Taxi): 
            self.f = (self.f+0.1)%self.F
        elif isinstance (self, Viper): 
            self.f = (self.f+0.1)%self.F
        elif self.vx != 0:
            self.f = (self.f+0.3)%self.F
        else:
            self.f = 3
    
        if self.dir > 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
    
class f1Car(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False,DOWN:False}
        self.powerup = False
        self.coin_sound = player.loadFile(path+"/Effects/coin.mp3")
        self.coin_count = 0
        
    def update(self):
        if self.y + self.r > game.h:
            self.y = game.h - 60
        
        self.velocity()    
        if self.keyHandler[RIGHT]:
            self.vx = 10
            self.dir = 1
        elif self.keyHandler[UP]:
            self.vy = -4
            self.dir = 1
        elif self.keyHandler[DOWN]:
            self.vy = 4
            self.dir = 1
            
        if self.x > game.w/2:
            game.x += self.vx
            
        for s in game.coins:
                if self.distance(s) <= self.r + s.r:
                    game.coins.remove(s)
                    del s
                    self.coin_sound.rewind()
                    self.coin_sound.play()
                    self.coin_count += 1
        
        #need to implement a collision detection, basically a for loop i think
        
    def distance(self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class Ambulance(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -2.5
        self.dir = 1
    
    def update(self):
        self.x += self.vx
        
class Police(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -3.5
        self.dir = 1
    
    def update(self):
        self.x += self.vx
 
class Taxi(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -2
        self.dir = 1
    
    def update(self):
        self.x += self.vx

class Viper(Vehicle):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -5
        self.dir = 1
    
    def update(self):
        self.x += self.vx
        
class Coin:
    def __init__(self,x,y,r,img,w1,h1,F,t):
        self.x = x
        self.y = y
        self.r = r
        self.w1 = w1
        self.h1 = h1
        self.F = F
        self.f = 0
        self.t = t
        self.img = loadImage(path+"/Images/coins.png")
        self.dir = 1
        
    def update(self):
        self.t = self.t + 1

    def display(self):
        self.update()
        self.f = (self.f+0.125)%self.F
        
        if self.dir > 0:
            image(self.img,self.x-self.w1//2-game.x,self.y-self.h1//2,self.w1,self.h1,int(self.f)*self.w1,0,int(self.f+1)*self.w1,self.h1)
        elif self.dir < 0:
            image(self.img,self.x-self.w1//2-game.x,self.y-self.h1//2,self.w1,self.h1,int(self.f+1)*self.w1,0,int(self.f)*self.w1,self.h1)

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
        self.f1Car = f1Car(50,665,20,self.g,"f1Car.png",110,80,1)
        self.background_images=[]
        for i in range(6,0,-1):
            self.background_images.append(loadImage(path+"/Images/layer"+str(i)+".png"))
        
        #game assets
        self.enemies=[] #<--- Need to modify enemy spawn intensity into a for loop or sth 
        self.enemies.append(Police(2000,665,80,self.g,"police.png",130,80,3,self.x,0))
        self.enemies.append(Ambulance(2500,760,80,self.g,"ambulance.png",150,80,3,self.x,0))
        self.enemies.append(Taxi(3000,665,850,self.g,"taxi.png",110,80,1,self.x,0))
        self.enemies.append(Viper(2500,665,575,self.g,"viper.png",110,80,1,self.x,0))
        self.enemies.append(Police(5000,665,80,self.g,"police.png",130,80,3,self.x,0))
        self.enemies.append(Ambulance(6500,760,80,self.g,"ambulance.png",150,80,3,self.x,0))
        self.enemies.append(Taxi(8000,665,850,self.g,"taxi.png",110,80,1,self.x,0))
        self.enemies.append(Viper(9500,665,575,self.g,"viper.png",110,80,1,self.x,0))
        
        self.coins = [] #<--- Need to modify coin spawn into a for loop or sth
        for i in range(10):
            self.coins.append(Coin(350+i*100,665,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(1500+i*100,760,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(3000+i*100,850,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(5000+i*100,760,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(6500+i*100,850,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(8000+i*100,575,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(9500+i*100,665,20,"coins.png",40,40,6,6))
        
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
        for img in self.background_images:
            x = (game.x//cnt)%game.w
            image(img,0-x,0)
            image(img,self.w-x,0)
            cnt-=1
        
        for enemy in self.enemies:
            enemy.display()
            
        for coin in self.coins:
            coin.display()
            
        self.f1Car.display()
        
        fill(255,255,255) 
        textSize(26)
        text("Score:",0,40) #<--- Need to make a function that increments score as game progresses
        fill(200,200,200)
        textSize(26)
        text(0+self.f1Car.coin_count*15,80,40)
    
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
