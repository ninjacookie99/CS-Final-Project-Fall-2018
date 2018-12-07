add_library('minim')
import os,time
path = os.getcwd()
player = Minim(this)

class Object:
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
    
    def velocity(self):
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
    
class f1Car(Object):
    def __init__(self,x,y,r,g,img,w,h,F):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False,DOWN:False}
        self.power_up = False
        self.coin_sound = player.loadFile(path+"/Effects/coin.mp3")
        self.death_sound = player.loadFile(path+"/Effects/death.mp3")
        self.coin_count = 0
        self.score_count = 0
       
    def update(self):
        if self.y + self.r+20 > game.h: #lower absolute bound
            self.y = game.h - 45
        elif self.y + self.r-55 < game.g: #upper absolute bound
            self.y = game.g + 46
        
        self.velocity() #implements velocity function for f1Car
        if self.keyHandler[RIGHT]:
            self.vx = 7 
            self.dir = 1
        elif self.keyHandler[UP]:
            self.vy = -3
            self.dir = 1
        elif self.keyHandler[DOWN]:
            self.vy = 3
            self.dir = 1
        
        if self.x > 5000: #changes f1Car velocity to 10
                self.vx = 10
        if self.x > 25000:
                self.vx = 13 #changes f1Car velocity to 13
                if self.keyHandler[UP]:
                    self.vy = -4 #changes f1Car upward velocity to 4
                    self.dir = 1
                elif self.keyHandler[DOWN]: 
                    self.vy = 4  #changes f1Car downward velocity to 4
                    self.dir = 1
                    
        if self.x > 40000 :
                self.vx = 15 #changes f1Car velocity to 10
                
        if self.x > game.w/2:
            game.x += self.vx #creates movement illusion as f1Car reaches half of the screen
            
        for c in game.coins: #coin collection by f1Car
                if self.distance(c) <= self.r + c.r:
                    game.coins.remove(c)
                    del c #removes coins off the screen
                    self.coin_sound.rewind()
                    self.coin_sound.play()
                    self.coin_count += 1
        
        for s in game.score: #accumulates score as f1Car travels in x direction
            if self.x > 100:
                self.score_count+= 2
                
        for e in game.enemies: #collision detection
            if self.distance(e) <= self.r + e.r:
                    self.death_sound.rewind()
                    self.death_sound.play()
                    game.music.pause()
                    game.f1Sound.pause()
                    game.lose = True #work on the collision detection, i think we have to use rectangles

    def distance(self,e): #algorithm for collision detection
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class Ambulance(Object):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -2.5
        self.dir = 1
    
    def update(self):
        self.x += self.vx #velocity function for ambulance
        
class Police(Object):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -3.5
        self.dir = 1
    
    def update(self):
        self.x += self.vx #velocity function for Police
 
class Taxi(Object):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -2
        self.dir = 1
    
    def update(self):
        self.x += self.vx #velocity function for Taxi

class Viper(Object):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -5
        self.dir = 1
    
    def update(self):
        self.x += self.vx #velocity function for Viper

# class Explosion(Object):
#     def __init__(self,x,y,r,
                 
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
        self.game_state = "play"
        self.lose = False
        self.win = False

        #images
        self.win_img = loadImage(path+"/Images/win.jpg")
        self.lose_img = loadImage(path+"/Images/gameover.png")
        self.f1Car = f1Car(50,665,20,self.g,"f1Car.png",110,80,1)
        self.background_images=[]
        for i in range(6,0,-1):
            self.background_images.append(loadImage(path+"/Images/layer"+str(i)+".png"))
        
        #game assets
        self.enemies=[] #<--- Need to modify enemy spawn intensity into a for loop or sth 
        self.enemies.append(Police(2000,665,100,self.g,"police.png",130,80,3,self.x,0))
        self.enemies.append(Ambulance(2500,760,100,self.g,"ambulance.png",150,80,3,self.x,0))
        self.enemies.append(Taxi(3000,665,100,self.g,"taxi.png",110,80,1,self.x,0))
        self.enemies.append(Viper(2500,570,100,self.g,"viper.png",110,80,1,self.x,0))
        self.enemies.append(Police(5000,665,100,self.g,"police.png",130,80,3,self.x,0))
        self.enemies.append(Ambulance(6500,760,100,self.g,"ambulance.png",150,80,3,self.x,0))
        self.enemies.append(Taxi(8000,665,100,self.g,"taxi.png",110,80,1,self.x,0))
        self.enemies.append(Viper(9500,665,100,self.g,"viper.png",110,80,1,self.x,0))
        
        self.coins = [] #<--- Need to modify coin spawn into a for loop or sth
        for i in range(10):
            self.coins.append(Coin(350+i*100,665,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(1500+i*100,760,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(3000+i*100,850,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(5000+i*100,760,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(6500+i*100,850,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(8000+i*100,575,20,"coins.png",40,40,6,6))
            self.coins.append(Coin(9500+i*100,665,20,"coins.png",40,40,6,6))
        
        self.score = [0]
        
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
        for img in self.background_images: #displays parallax background on screen
            x = (game.x//cnt)%game.w
            image(img,0-x,0)
            image(img,self.w-x,0)
            cnt-=1
        
        for enemy in self.enemies: #displays enemies on screen
            enemy.display()
            
        for coin in self.coins: #displays coins on screen
            coin.display()
            
        self.f1Car.display() #displays f1Car on screen
        
        fill(255,255,255) 
        textSize(26)
        text("Score:",0,40)
        fill(200,200,200)
        textSize(26)
        text((0+self.f1Car.coin_count*100)+(self.f1Car.score_count),80,40) #shows score on top left of screen (distance + coin )
    
game = Game(1440,900,519)

def setup():
    size(game.w,game.h)
    background(0)
    
def draw():
    stroke(255)
    line(0,game.g,1440,game.g)
  
    if game.pause != True and game.game_state == "play":
        game.display()
    elif game.pause == True:
        textSize(30)
        fill(255,0,0)
        text("Paused",game.w//2,game.h//2)
        
def keyPressed():
    if keyCode == LEFT:
        game.f1Car.keyHandler[LEFT]=True
    elif keyCode == RIGHT:
        game.f1Car.keyHandler[RIGHT]=True
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
            game.f1Sound.pause()
        else:
            game.music.play()
            game.f1Sound.play()

def keyReleased():  
    if keyCode == UP:
        game.f1Car.keyHandler[UP]=False
    elif keyCode == DOWN:
        game.f1Car.keyHandler[DOWN]=False
    elif keyCode == LEFT:
        game.f1Car.keyHandler[LEFT]=False
    elif keyCode == RIGHT:
        game.f1Car.keyHandler[RIGHT]=False
