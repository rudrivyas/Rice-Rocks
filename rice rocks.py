import simplegui
import math
import random
WIDTH = 800
HEIGHT = 600
started=False
score = 0
lives = 5
time = 0
age = 0
missile_group=set([])
rock_group=set([])
rmst=set([])
#explosion_image = simplegui.load_image("D:\explosion.hasgraphics.png")

class ImageInfo:
    def __init__(self,center,size,radius=0,lifespan=None,animated=False):
        self.center=center
        self.size=size
        self.radius=radius
        self.animated=animated
        self.lifespan=lifespan
            
    def get_center(self):
            return self.center
    def get_size(self):
            return self.size
    def get_radius(self):
            return self.radius
    def get_lifespan(self):
            return self.lifespan
    def get_animated(self):
            return self.animated
        
debris_info = ImageInfo([320, 240], [640, 480])  #object of image info
debris_image = simplegui.load_image("D:\debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("D:/nebula_blue.png")


splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("D:\splash.png")

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("D:\double_ship.png")

missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("D:\shot2.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("D:\asteroid_blue.png")

#explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
#explosion_image = simplegui.load_image("D:\explosion_alpha.png")

soundtrack = simplegui.load_sound("D:\soundtrack.mp3")
missile_sound = simplegui.load_sound("D:\missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("D:\thrust.mp3")
explosion_sound = simplegui.load_sound("D:\explosion.mp3")

def angle_to_vector(ang):
    return [math.cos(ang),math.sin(ang)]


def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

class ship:
    
    def __init__(self,vel,pos,angle,image,info):
        self.pos=[pos[0],pos[1]]
        self.vel=[vel[0],vel[1]]
        self.angle=angle
        self.thrust=False
        self.ang_vel=0
        self.image=image
        self.radius=info.get_radius()
        self.image_size=info.get_size()
        self.image_center=info.get_center()
        
    def draw(self,canvas):
        if self.thrust==True:
            canvas.draw_image(self.image,[self.image_center[0]+self.image_size[0], self.image_center[1]],self.image_size,self.pos,self.image_size,self.angle)
            
            
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
            
    def update(self):
        self.angle+=self.ang_vel
        
        self.pos[0]=(self.pos[0]+self.vel[0])%WIDTH
        self.pos[1]=(self.pos[1]+self.vel[0])%HEIGHT
        
        if self.thrust==True:
            acc=angle_to_vector(self.angle)
            self.vel[0]+=acc[0]*0.25
            self.vel[1]+=acc[1]*0.25
            
        self.vel[0]*=0.96
        self.vel[1]*=0.96
    
    
    
    def set_thrust(self,on):
        self.thrust=on
        if on==True:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            
    
    
    def get_position(self):
        return self.pos
    def increment_angle_vel(self):
        self.ang_vel+=0.05
        
    def decrement_angle_vel(self):
        self.ang_vel -=0.05

        
    def shoot(self):
        global missile_group
        forward=angle_to_vector(self.angle)
        missile_pos=[self.pos[0]+self.radius*forward[0],self.pos[1]+self.radius*forward[1]]
        missile_vel=[self.vel[0]+6*forward[0],self.vel[1]+6*forward[1]]
        missile_group.add(sprite(missile_pos,missile_vel,self.angle,0,missile_image,missile_info,missile_sound))
        
        

        
class sprite:  #missile and rock
    def __init__(self,pos,vel,ang,ang_vel,image,info,sound=None):
        self.pos=[pos[0],pos[1]]
        self.vel=[vel[0],vel[1]]
        self.angle=ang
        self.angle_vel=ang_vel
        self.image=image
        self.radius=info.get_radius()
        self.image_size=info.get_size()
        self.image_center=info.get_center()
        self.lifespan=info.get_lifespan()
        self.animated=info.get_animated()
        self.age=0
       # sound=on
        if sound==True:
            sound.rewind()
            sound.play()
            
    def draw(self,canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
            
    def get_position(self):
        return self.pos
   
    def update(self):
        
        self.angle+=self.angle_vel
        self.age+=1
        self.pos[0]=(self.pos[0]+self.vel[0])%WIDTH
        self.pos[1]=(self.pos[1]+self.vel[1])%HEIGHT
        
    def collide(self,other_object):
        c1=self.get_position()
        c2=other_object.get_position()
        if distance(c1,c2)<(self.radius+other_object.radius):
            return True
        else:
            return False
        
def gr_group_collide(): #missile and rock
    global score
    rock_set=set([])
    missile_set=set([])
    for m  in missile_group:
        for r in rock_group:
            if r.collide(m):
                score+=10
                rock_set.add(r)
                missile_set.add(m)
                
   
            if len(missile_set)>0:
                missile_group.difference_update(missile_set)
            if len(rock_set)>0:
                rock_group.difference_update(rock_set)
 
def group_collide(): #rock only
    global lives,started
    rock_set=set([])
    missile_set=set([])
    for r in rock_group:
         if r.collide(my_ship):
            lives-=1
            if lives==0:
                started=False
                soundtrack.pause()
                rock_set=rock_group.copy()
            rock_set.add(r)
    rock_group.difference_update(rock_set)
        
def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
        
def keydown(key):
    if key==simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
        
    elif key==simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
        
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
        
    elif key==simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
    
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
        
    elif key==simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
        
    elif key==simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        

def click(pos):
    global started,lives,score
    score=0
    lives=5
    center=[WIDTH/2,HEIGHT/2]
    size=splash_info.get_size()
    in_width=(center[0]-size[0])<pos[0]<(center[0]+size[0])
    in_height=(center[1]-size[1])<pos[1]<(center[1]+size[1])
    if (not started) and   in_width  and  in_height:
        started=True
        soundtrack.rewind()
        soundtrack.play()
        
        
        
def rock_spawner():
    global rock_group,started,score
    if started==True:
        rock_pos=[random.randrange(0,WIDTH),random.randrange(0,HEIGHT)]
        rock_vel=[random.randrange(-4,4)*0.6-0.3,random.randrange(-4,4)*0.6-0.3]
        if score>100:
            rock_vel[0]*=2
            rock_vel[1]*=2
        rock_avel=random.random()*.2 -.1    
        
    
        if len(rock_group)<12:
            if distance(rock_pos,my_ship.pos)>100:
                rock_group.add(sprite(rock_pos,rock_vel,0,rock_avel,asteroid_image,asteroid_info))
def draw(canvas):
    global started,lives,HEIGHT,WIDTH,time,info,age
    group_collide()
    gr_group_collide()
    time+=1
    wtime=(time/4)%WIDTH
    center=debris_info.get_center()
    size=debris_info.get_size()
    
    canvas.draw_image(nebula_image,nebula_info.get_center(),nebula_info.get_size(),[WIDTH/2,HEIGHT/2],[WIDTH,HEIGHT])
    canvas.draw_image(debris_image,center,size,(wtime-WIDTH/2,HEIGHT/2),(WIDTH,HEIGHT))
    canvas.draw_image(debris_image,center,size,(wtime+WIDTH/2,HEIGHT/2),(WIDTH,HEIGHT))
        
    

    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    my_ship.draw(canvas)
    for r in rock_group:
        r.draw(canvas)
        
    for m in missile_group:
        rock_set=set([])
        m.draw(canvas)
        if m.age>m.lifespan:
            rock_set.add(m)
        missile_group.difference_update(rmst)
        missile_group.difference_update(rock_set)
        
        my_ship.update()
        for r in rock_group:
            r.update()
        for m in missile_group:
            m.update()
            
    if (not started):
        canvas.draw_image(splash_image,splash_info.get_center(),splash_info.get_size(),[WIDTH/2,HEIGHT/2],splash_info.get_size())

        


my_ship=ship([0,0],[WIDTH/2,HEIGHT/2],0,ship_image,ship_info)
a_rock=sprite([WIDTH/3,HEIGHT/3],[1,1],0,0.1,asteroid_image,asteroid_info)
a_missile=sprite([2*WIDTH/3,2*HEIGHT/3],[-1,-1],0,0,missile_image,missile_info)
        
frame=simplegui.create_frame("asteroids",WIDTH,HEIGHT)       
    
soundtrack.play()      
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
timer=simplegui.create_timer(1000,rock_spawner)        
        
frame.start()
timer.start()
