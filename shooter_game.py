# Создай собственный Шутер!
import pygame as pg
import constants as cnst
import random
import pygame_menu as menu


class GameSprite(pg.sprite.Sprite):
    def __init__(self, image, width, height, x, y, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pg.K_d] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.x + 33, self.rect.y, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        if self.rect.y < cnst.WIDTH_WINDOW:
            self.rect.y += self.speed
        else: 
            global enemy_finish 
            enemy_finish += 1
            self.rect.y = 0
            self.rect.x = random.randint(30, cnst.HEIGHT_WINDOW - 30)

class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()

def start_game():
    global main_menu
    main_menu.disable()
    main_menu.full_reset()


pg.init()
window = pg.display.set_mode((cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW))
pg.display.set_caption("Space game")
game = True
finish = False
enemy_finish = 0
clock = pg.time.Clock()
background = pg.transform.scale(pg.image.load('galaxy.jpg'), \
    (cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW))
pg.mixer.init()
pg.mixer.music.load('space.ogg')
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play()
fire_sound = pg.mixer.Sound('fire.ogg')
player = Player('rocket.png', 80, 100, 5, 400, 10)
monsters = pg.sprite.Group()
bullets = pg.sprite.Group()
main_menu = menu.Menu('Space Game', cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW)
main_menu.add.button('PLAY', start_game)
main_menu.add.button('EXIT', menu.events.EXIT)
pg.font.init()
font = pg.font.Font(None, 36)
for i in range(5):
    monster = Enemy('ufo.png', 80, 50, random.randint(30, cnst.HEIGHT_WINDOW - 30), random.randint(20, 30), random.randint(1, 3))
    monsters.add(monster)
    
while game:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            game = False
        elif i.type == pg.MOUSEBUTTONDOWN and i.button == 1:
            fire_sound.play()
            player.fire()
             
    if main_menu.is_enabled():
        main_menu.mainloop(window)
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        count = font.render('Счет:', 1, (255, 255, 255))
        window.blit(count, (10, 20))
        lose = font.render(f'Пропущено: {enemy_finish}', 1, (255, 255, 255))
        window.blit(lose, (10, 50))
        if enemy_finish >= 3:
            finish = True
            main_menu.enable()
    pg.display.update()
    clock.tick(cnst.FPS)
