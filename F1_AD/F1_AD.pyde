add_library('minim')
import os,random
path = os.getcwd()
player = Minim(this)

# class Vehicle():
#     def __init__(self,x,y,r,g,img,w,h,F):
#         self.x=x
#         self.y=y
#         self.r=r
#         self.g=g
#         self.vx=0
#         self.w=w
#         self.h=h
#         self.F=F
#         self.f=0
#         self.img= loadImage(path+"/Images/"+img)
#         self.dir = 1
        
# class f1Car(Vehicle):
#     def __init__(self,x,y,r,g,img,w,h,F):
#         Vehicle.__init__(self,x,y,r,g,img,w,h,F)
#         self.keyHandler={LEFT:False, RIGHT:False, UP:False,DOWN:False}
              
# class Truck(Vehicle):
#     def __init__(self,x,y,r,g,img,w,h,F):
#         Vehicle.__init__(self,x,y,r,g,img,w,h,F)
        
# class Sedan(Vehicle):
#     def __init__(self,x,y,r,g,img,w,h,F):
        
# class Car(Vehicle):
#     def __init__(self,x,y,r,g,img,w,h,F):
        
# class Coin():
#     def __init__(self,x,y,r,g,img,w,h,F):
        
class Game:
    def __init__(self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.x=0
        self.pause = False
        self.pauseSound = player.loadFile(path+"/Sounds/pause.mp3")
        # self.music = player.loadFile(path+"/sounds/backgroundmusic.mp3")
        # self.music.play()
    
#     self.bgImgs=[]
#         for i in range(5,0,-1):
#             self.bgImgs.append(loadImage(path+"/images/layer_0"+str(i)+".png"))
    
#     self.f1Car = f1Car(50,50,35,self.g,"f1.png",100,70,11)
    
#     self.enemies = []
    
    # def display(self):
    #     cnt = 5
    #     for img in self.bgImgs:
    #         x = (game.x//cnt)%game.w
    #         image(img,0-x,0)
    #         image(img,self.w-x-1,0)
    #         cnt-=1
            
    #     for p in self.platforms:
    #         p.display()
        
    #     for e in self.enemies:
    #         e.display() 
               
    #     self.mario.display()

game = Game(1280,1080,585)

def setup():
    size(game.w,game.h)
    stroke(255)
    background(0)
    

def draw():
    line(0,game.g,1280,game.g)
    line(0,game.g-200,1280,game.g-200)
    ellipse(0,game.g,50,50)
    
    # if game.pause == False:
    #     background(0)
    #     game.display()
    # else:
    #     textSize(50)
    #     fill(255,0,0)
    #     text("Paused",game.w//2,game.h//2)
    
# def mouseClicked():
    
# def keyPressed():
    
# def keyReleased():
