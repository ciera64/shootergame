from pygame import *
from random import randint
from time import sleep

window = display.set_mode((700,500)) 
display.set_caption("Shooter")
fps = time.Clock()
bg= transform.scale(image.load("bridge.jpg"),(700,500))
lost =0
score = 0

font.init()
font2 = font.SysFont("Impact",40)
font3 = font.SysFont("Impact",74)

mixer.init()
mixer.music.load("mondt.mp3")
mixer.music.play()

class Gamespite(sprite.Sprite):
    def __init__(self,img,x,y,speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(img),(width,height))
        self.x = x 
        self.y = y
        self.direction = "left"
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(Gamespite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x <700-5:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("arrikw.png",self.rect.x,self.rect.top,20,65,65)
        bullets.add(bullet)

class Enemy(Gamespite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= (500):

            self.rect.y = 0
            lost = lost + 1

class Bullet(Gamespite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

p1 = Player("yelan22.png",350,(500-130),10,65,120)

enemys = sprite.Group()
for i in range(1,6):
    e = Enemy("birb.png",randint(65,(700-65)),(65),randint(1,4),65,65)
    enemys.add(e)

bullets = sprite.Group()

game = True
while game is True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                p1.fire()
                f1 = mixer.Sound("arrow.mp3")
                f1.play()
              
    window.blit(bg,(0,0))
    p1.reset()
    p1.update()
    enemys.update()
    bullets.update()
    fps.tick(60)
    text_missed = font2.render("Missed: " + str(lost), 1, (255,255,255))
    text_scored = font2.render("Score: " + str(score), 1, (255,255,255))
    window.blit(text_missed,(20,60))
    window.blit(text_scored,(20,20))
    enemys.draw(window)
    bullets.draw(window)

    if lost > 10 or sprite.spritecollide(p1,enemys,False):
        lose = font3.render("YOU LOSE",True,(255,0,0))
        window.blit(lose,(250,250))
        display.update()
        
        sleep(3)
        game = False

    if sprite.spritecollide(p1,enemys,False):
        game = False

    if sprite.groupcollide(bullets,enemys,True,True):
        score += 1
        e = Enemy("birb.png",randint(65,(700-65)),(65),randint(1,4),65,65)
        enemys.add(e) 

    if score > 10:
        win = font3.render("YOU WIN",True,(0,255,0))
        window.blit(win,(250,250))
        display.update()

        sleep(3)
        game = False
        
    display.update()