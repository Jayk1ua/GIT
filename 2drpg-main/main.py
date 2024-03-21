#import
from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint, shuffle, choice

#window
win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))

#image
background = display.set_mode((win_width, win_height))
display.set_caption('Health Bar')
#fps
background = scale(load('background.jpg'), (win_width, win_height))
clock = time.Clock()
FPS = 60

background_menu = scale(load('background_menu.jpg'), (win_width, win_height))

#sound
mixer.init()
mixer.music.load('backgroundmusic.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)

lost = 0
score = 0

#GameSprite + класи
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = scale(load(player_image), (player_width, player_height))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    
    hp = 3
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        #if keys[K_DOWN] and self.rect.y < win_height - 80:
            #self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        
    


    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx + 15, self.rect.centery - 12, 25, 35, 15)
        bullets.add(bullet)



class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.kill()

class Enemy(GameSprite):
    
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x>win_width:
            self.rect.x=0
            self.rect.x=randint(800, 490)
            lost = lost + 1

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
  
        ratio = self.hp / self.max_hp
        draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
            
health_bar = HealthBar(0, 80, 300, 40, 100)

health_bar.hp = 100

#Текст  
font.init()
font1 = font.SysFont('Arial', 36)

txt_win = font1.render('Ти виграв', True, (0, 225, 0))



#objects
ground = GameSprite('background.jpg', 0, 560, 800, 110, 0)

zombie = ['zombie1.png', 'zombie2.png']

bullets = sprite.Group()

mplayer = Player('mplayer.png', 200, 490, 90, 70, 5)            

button = GameSprite('startbutton.png',120,135,120,110,0)

monsters = sprite.Group()
for i in range(5):
    mon = Enemy(choice(zombie), 800, 498,  80, 60, randint(1, 5))
    monsters.add(mon)

menu = True

#Ігровий цикл
def main():
    lost = 0
    score = 0
    run = True
    finish = False
    mixer_music.stop()
    mixer.music.load('background_music.ogg')
    mixer.music.play()
    mixer.music.set_volume(0.1)

    window.blit(background,(0, 0))
    mplayer.reset()
    mplayer.update()
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    mplayer.fire()
                    fire_sound.play()
                    

        if not finish:
            
            
            window.blit(background,(0, 0))

            bullets.draw(window)
            bullets.update()


            txt_lose = font1.render(f'Пропущено: {lost}', True, (255,0,0))
            window.blit(txt_lose, (10, 40))


            mplayer.reset()
            mplayer.update()

            monsters.draw(window)
            monsters.update()

            health_bar.draw(window)
            
            
            
            if not sprite.collide_rect(mplayer, ground):
                mplayer.rect.y += 2.5

            

            if sprite.spritecollide(mplayer, monsters, True, ):
                lost = lost + 1
                score = score + 1
                health_bar.hp = health_bar.hp - 10
                
                if score < 10:
                    mon = Enemy(choice(zombie), 800, 497,  80, 60, randint(1, 5))
                    monsters.add(mon)
                    

                if health_bar.hp == 0:
                    finish = True
                
                


            
            collides = sprite.groupcollide(monsters, bullets, True, True)

            
            
            if score < 10:
                
                for c in collides:
                    mon = Enemy(choice(zombie), 800, 497,  80, 60, randint(1, 5))
                    monsters.add(mon)
                    score = score + 1

                
                    
                    
                
            

        else:

            for b in bullets:
                b.kill()

            for m in monsters:
                m.kill()





        display.update()
        clock.tick(FPS)
        


while menu:
    for e in event.get():
        if e.type == QUIT:
            menu = False
        if e.type == MOUSEBUTTONDOWN and e.button==1:
            x,y = e.pos
            if button.rect.collidepoint(x,y):
                menu=False
                main()
                
                
    window.blit(background_menu,(0, 0))
    button.reset()
    

    display.update()
    time.delay(50)