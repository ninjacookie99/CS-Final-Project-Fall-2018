add_library('minim')
import os,time
import random
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
        self.shield = False
       
    def update(self):  #updates each frame based on the velocity function
        self.velocity()
    
    def velocity(self): #velocity function for each vehicle on the screen
        self.x += self.vx
        self.y += self.vy
       
        if self.y+self.r < self.g:
            self.vy = 0
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0 
        self.vx += 0.005 #increases the speed of the f1Car as the game progresses
     
    def display(self):
        self.update()
        
        # displays frames for various instances...
        if isinstance (self, Police):
            self.f = (self.f+0.1)%self.F
        elif isinstance (self, Ambulance):
            self.f = (self.f+0.1)%self.F
        elif isinstance (self, Taxi): 
            self.f = (self.f+0.1)%self.F
        elif isinstance (self, Viper): 
            self.f = (self.f+0.1)%self.F
        elif isinstance (self, Explosion): 
            self.f = (self.f+0.1)%self.F
        elif isinstance (self, f1Car):
            if self.shield == True and self.f < 4:
                self.f = (self.f+0.2)%self.F
            elif self.shield == 1:
                self.f = 4
            else:
                self.f = 0
                
        if self.dir > 0: #displays the image of the desired object based on the direction
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,self.h * self.shield,int(self.f+1)*self.w,self.h * (self.shield + 1))
        elif self.dir < 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,self.h * self.shield,int(self.f)*self.w,self.h * (self.shield + 1) )

class f1Car(Object):
    def __init__(self,x,y,r,g,img,w,h,F):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False,DOWN:False}
        self.power_up = False
        self.coin_sound = player.loadFile(path+"/Effects/coin.mp3")
        self.powerup_sound = player.loadFile(path+"/Effects/powerup.mp3")
        self.death_sound = player.loadFile(path+"/Effects/death.mp3")
        self.coin_count = 0
        self.score_count = 0
        self.powerup_count = 0
        self.shield = False
        self.game_end = 80#seconds taken to end the game and refresh
        
    def update(self):
        if self.y + self.r+20 > game.h: #lower absolute bound
            self.y = game.h - 45
        elif self.y + self.r-55 < game.g: #upper absolute bound
            self.y = game.g + 46
        
        if self.shield != True:    
            self.velocity() #implements velocity function for f1Car
            if self.keyHandler[RIGHT]:
                    self.vx = 7 
                    self.dir = 1
            elif self.keyHandler[UP]:
                    self.vy = -6
                    self.dir = 1
            elif self.keyHandler[DOWN]:
                    self.vy = 6
                    self.dir = 1
        else:
            self.velocity()
            if self.keyHandler[RIGHT]:
                    self.vx = 7 
                    self.dir = 1
            elif self.keyHandler[UP]:
                    self.vy = -6
                    self.dir = 1
            elif self.keyHandler[DOWN]:
                    self.vy = 6
                    self.dir = 1
                
        if self.x > game.w/2:
            game.x += self.vx #creates movement illusion as f1Car reaches half of the screen
                
        for c in game.coins: #coin collection by f1Car
                if self.distance(c) <= self.r + c.r:
                    game.coins.remove(c)
                    del c #removes coins off the screen
                    self.coin_sound.rewind()
                    self.coin_sound.play()
                    self.coin_count += 1
                    
        for p in game.powerups: #powerup collection by f1Car
                if self.distance(p) <= self.r + p.r:
                    game.powerups.remove(p)
                    del p #removes powerup off the screen
                    self.powerup_sound.rewind()
                    self.powerup_sound.play()
                    self.powerup_count += 1
                    
        for s in game.score: #accumulates score as f1Car travels in x direction
            if self.x > 100 and game.lose == False:
                self.score_count+= 5
                
        for e in game.enemies: #collision detection
            if self.distance(e) <= self.r + e.r:
                if self.shield == True:  #removes shield power up and displays explosion on collision
                    self.shield = False
                    game.enemies.remove(e)
                    game.explosions.append(Explosion(e.x,e.y,50,0,"explosion.png",80,100,10))
                    self.death_sound.rewind()
                    self.death_sound.play()
                    del e
                else:  #displays explosion on collision
                    game.enemies.remove(e) 
                    game.explosions.append(Explosion(e.x,e.y,50,0,"explosion.png",80,100,10))
                    self.vx = 0
                    self.death_sound.rewind()
                    self.death_sound.play()
                    game.music.pause()
                    game.f1Sound.pause()
                    game.lose = True
                    game.win = False
                    del e
                    return
            
        #returns back to the menu if game is lost
        if game.lose == True and game.win == False:
            self.game_end -= 1
            print self.game_end
            if self.game_end == 0:
                game.__init__(1440,900,519)

    def distance(self,e): #algorithm for collision detection
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class Ambulance(Object): #ambulance class
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -3.5
        self.dir = 1
        
    def update(self): 
        self.x += self.vx #velocity function for ambulance
        self.vx -= 0.002
                
    def distance(self,e): #algorithm for collision detection
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
    
class Police(Object): #police car class
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -4.5
        self.dir = 1
        
    def update(self):
        self.x += self.vx #velocity function for Police
        self.vx -= 0.002
        
    def distance(self,e): #algorithm for collision detection
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
 
class Taxi(Object):  #taxi class
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -2
        self.dir = 1
      
    def update(self):
        self.x += self.vx #velocity function for Taxi
        self.vx -= 0.0001
    
    def distance(self,e): #algorithm for collision detection
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
        
class Viper(Object): #dodge viper class
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = -5
        self.dir = 1
    
    def update(self):
        self.x += self.vx #velocity function for Viper
        self.vx -= 0.003
        
    def distance(self,e): #algorithm for collision detection
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class Explosion(Object): #explosion class
    def __init__(self,x,y,r,g,img,w,h,F):
        Object.__init__(self,x,y,r,g,img,w,h,F)
        
    def update(self):
        if int(self.f) == 9: 
            game.explosions.remove(self) #removes explosion frames from the screen
            del self
            return
                 
class Coin: #coin class
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

    def update(self):
        self.t = self.t + 1

    def display(self):
        self.update()
        self.f = (self.f+0.250)%self.F #displays coin frames on the screen
        
        #displays coin image on the screen
        image(self.img,self.x-self.w1//2-game.x,self.y-self.h1//2,self.w1,self.h1,int(self.f)*self.w1,0,int(self.f+1)*self.w1,self.h1)
            
class PowerUp: #powerup token class 
    def __init__(self,x,y,r,img,w1,h1,F,t):
        self.x = x
        self.y = y
        self.r = r
        self.w1 = w1
        self.h1 = h1
        self.F = F
        self.f = 0
        self.t = t
        self.img = loadImage(path+"/Images/powerup.png")
        
    def update(self):
        self.t = self.t + 1

    def display(self):
        self.update()
        self.f = (self.f+0.350)%self.F #displays powerup frames on the screen
        
        #displays powerup image on the screen
        image(self.img,self.x-self.w1//2-game.x,self.y-self.h1//2,self.w1,self.h1,int(self.f)*self.w1,0,int(self.f+1)*self.w1,self.h1)

class Game: #main game class  
    def __init__(self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.x=0
        
        #initial states for the game
        self.pause = False
        self.state = "menu" 
        self.lose = False 
        self.win = False
        
        self.f1Car = f1Car(50,665,20,self.g,"f1Car.png",132,100,4) #creates f1Car object for the game class
        
        #gameimages
        self.menubackground = loadImage(path+"/Images/menubackground.png")
        self.instructions = loadImage(path+"/Images/instructions.jpg")
        
        self.background_images=[] #loads all the background images into a list
        for i in range(6,0,-1):
            self.background_images.append(loadImage(path+"/Images/layer"+str(i)+".png"))
        
        #game assets
        self.enemies=[] #Stores all enemy objects into a list
        for j in range(50):
            for i in range(1):
                self.enemies.append(Police((1000)+j*2500+i*50,665,45,self.g,"police.png",130,80,3,self.x,0))
                self.enemies.append(Ambulance((1440)+j*5000+i*50,760,45,self.g,"ambulance.png",150,80,3,self.x,0))
                self.enemies.append(Taxi((3500)+j*7500+i*50,550,45,self.g,"taxi.png",110,80,1,self.x,0))
                self.enemies.append(Viper((5000)+j*10000+i*50,850,45,self.g,"viper.png",110,80,1,self.x,0))
                random.shuffle(self.enemies)
                        
        self.coins = [] #stores all Coin objects into a list
        for j in range(50):
            for i in range (10):
                self.coins.append(Coin((350)+j*2500+i*50,665,20,"coins.png",40,40,6,6)) 
                self.coins.append(Coin((1440)+j*5000+i*50,760,20,"coins.png",40,40,6,6))
                self.coins.append(Coin((3500)+j*7500+i*50,550,20,"coins.png",40,40,6,6))
                self.coins.append(Coin((5000)+j*10000+i*50,850,20,"coins.png",40,40,6,6))
                random.shuffle(self.coins)
            
        self.powerups = [] #stores all PowerUp objects into a list
        for x in range(50):
            for y in range (1):
                self.powerups.append(PowerUp((1200)+x*10000,550,30,"powerup.png",50,50,6,6)) 
                self.powerups.append(PowerUp((2400)+x*10000,665,30,"powerup.png",50,50,6,6))
                self.powerups.append(PowerUp((3600)+x*10000,850,30,"powerup.png",50,50,6,6))
                self.powerups.append(PowerUp((4800)+x*10000,760,30,"powerup.png",50,50,6,6))
                random.shuffle(self.powerups)

        self.score = [0]
        self.explosions = []
        
        #sounds
        self.pauseSound = player.loadFile(path+"/Effects/pause.mp3")
        self.music = player.loadFile(path+"/Effects/background.mp3")
        self.menuMusic = player.loadFile(path+"/Effects/menu.mp3")
        self.menuMusic.play()
        self.winSound = player.loadFile(path+"/Effects/win.mp3")
        self.loseSound = player.loadFile(path+"/Effects/lose.mp3")
        self.f1Sound = player.loadFile(path+"/Effects/formula1.mp3")

    def display(self):
        cnt = 6
        for img in self.background_images: #displays parallax background on screen
                x = (game.x//cnt)%game.w
                image(img,0-x,0)
                image(img,self.w-x,0)
                cnt-=1
        
        for enemy in self.enemies: #displays enemies on screen
                enemy.display()
        
        for e in self.explosions: #displays car explosion on collision
                e.display()
            
        for coin in self.coins: #displays coins on screen
                coin.display()
        
        for p in self.powerups: #displays powerup tokens on screen
                p.display()
            
        self.f1Car.display() #displays f1Car on screen
       
        fill(255,255,255)  #shows score on top left of screen (distance + coin + powerup)
        textSize(26)
        text("Score:",0,40)
        fill(200,200,200)
        textSize(26)
        text((0+self.f1Car.coin_count*1000)+(self.f1Car.score_count),80,40) 
       
        fill(255,255,255)  #shows powerup count on top left of screen
        textSize(26)
        text("Shields:",0,80)
        fill(0,0,0)
        textSize(26)
        text(self.f1Car.powerup_count,100,80) 
        
game = Game(1440,900,519) #Game object

def setup():
    size(game.w,game.h)
    background(0)
    frameRate(70)
    
def draw(): 
    font = loadFont("MS-PGothic-48.vlw")
    if game.state == "menu": #displays the menu screen
        image(game.menubackground,0,0)
        fill(0,0,0)
        
        rect(game.w//2.6,game.h//3.5,300,50)
        if game.w//2.6< mouseX <game.w//2.6+350 and game.h//3.5<mouseY<game.h//3.5+50:
            fill(0,0,255)        
        else:
            fill(255,255,255)
         
        textFont(font,58)
        text("Instructions",560,300) #displays the instructions button
        fill(0)
        
        rect(game.w//2.6,game.h//3.5+200,300,50)
        if game.w//2.6< mouseX <game.w//2.6+350 and game.h//3.5+200<mouseY<game.h//3.5+250:
            fill(0,0,255)        
        else:
            fill(255,255,255)
        textFont(font,58)
        text("Play Game",580,500)  #displays the play game button
    
    if game.state == "instructions":
        image(game.instructions,0,0,1440,900)
        fill(0,0,255)
        textFont(font,60)
        text("Instructions",game.w//2.2-60,100)
        fill(0,255,100)
        #Instructions for the game
        textFont(font,40)
        text("~Your goal is to avoid enemy cars and drive to score as much points as possible",100,200)
        text("~Collect coins to score extra points.",100,250)
        text("~Collect powerups to obtain extra points.",100,300)
        text("~Use the up and down arrow keys to move the f1 car across the road.",100,350)
        text("~Press the right arrow to start the F1 car and begin movement.",100,400)
        text("~Press spacebar to use the power up and P to pause the game.",100,450)
        text("~You may use powerups at the expense of points.",100,500)
         
        fill(0,0,0)
        rect(game.w//2.2,game.h//3.5+500,125,50)
        textSize(58)
        if game.w//2.6< mouseX <game.w//2.6+350 and game.h//3.5+500<mouseY<game.h//3.5+550:
            fill(255,0,0)        
        else:
            fill(255,255,255)
        text("Back",game.w//2.2,game.h//3.5+550) #displays back button on screen
        fill(0)               
        
    if game.state == "play" and game.pause == False:
        background(0)
        game.display()
    elif game.pause == True:
        textSize(30)
        fill(255,0,0)
        text("Paused",game.w//2,game.h//2)
    
def mouseClicked():
    if game.w//2.6< mouseX <game.w//2.6+350 and game.h//3.5<mouseY<game.h//3.5+50:
        game.state = "instructions" #goes to instruction screen once instructions button is clicked"
       
    if game.w//2.6< mouseX <game.w//2.6+350 and game.h//3.5+200<mouseY<game.h//3.5+250:
        game.menuMusic.pause()
        game.music.play()
        game.state = "play" #goes to gamescreen once the play game button is clicked
        
    if game.w//2.6< mouseX <game.w//2.6+350 and game.h//3.5+500<mouseY<game.h//3.5+550:
        game.state = "menu" #goes back to menu screen once back button is clicked
        
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
    elif keyCode == 32 and game.f1Car.powerup_count >= 1:
        game.f1Car.powerup_count -= 1#uses powerup once spacebar is pressed
        game.f1Car.shield = True
        game.f1Car.powerup_sound.rewind()
        game.f1Car.powerup_sound.play()
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
