import pygame as pg
import constants as cnst
import random
import pygame_menu as menu
from time import time as timer


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


class Asteroid(GameSprite):
    def update(self):
        if self.rect.y < cnst.WIDTH_WINDOW:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = random.randint(30, cnst.HEIGHT_WINDOW - 30)


def start_game():
    global main_menu
    main_menu.disable()
    main_menu.full_reset()


def main_background() -> None:
    window.blit(background_image, (0, 0))


pg.init()
pg.font.init()
pg.mixer.init()
clock = pg.time.Clock()

window = pg.display.set_mode((cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW))
pg.display.set_caption("Space game")
game = True
finish = False
enemy_finish = 0
reload_time = False
num_fire = 0
lose_enemy = 0

font = pg.font.SysFont('Arial', 36)
font_finish = pg.font.SysFont('Arial', 70)
win = font_finish.render('YOU WIN!!!', True, cnst.GREEN)
lose_finish = font_finish.render('YOU LOSE!!!', True, cnst.RED)

pg.mixer.music.load('space.ogg')
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play()
fire_sound = pg.mixer.Sound('fire.ogg')

background = pg.transform.scale(pg.image.load('galaxy.jpg'), \
    (cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW))
background_image = pg.image.load('menu_background.jpg')

main_menu = menu.Menu('Space Game', cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW)
main_menu.add.button('PLAY', start_game)
main_menu.add.button('EXIT', menu.events.EXIT)

player = Player('rocket.png', 80, 100, 5, 400, 10)
monsters = pg.sprite.Group()
bullets = pg.sprite.Group()
asteroids = pg.sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', 80, 50,
    random.randint(30, cnst.HEIGHT_WINDOW - 30),
    random.randint(20, 30), random.uniform(1.0, 2.2))
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid('asteroid.png', 80, 50,
    random.randint(30, cnst.HEIGHT_WINDOW - 30),
    random.randint(20, 30), 2)
    asteroids.add(asteroid)

while game:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            game = False
        elif i.type == pg.MOUSEBUTTONDOWN and i.button == 1:
            if num_fire < 10 and not reload_time:
                fire_sound.play()
                player.fire()
                num_fire += 1
            elif num_fire >= 10 and not reload_time:
                last_time = timer()
                reload_time = True

    if main_menu.is_enabled():
        main_menu.mainloop(window, main_background)
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        if (enemy_finish >= 3
            or pg.sprite.spritecollide(player, asteroids, False)
            or pg.sprite.spritecollide(player, monsters, False)):
            finish = True
            window.blit(lose_finish, (200, 200))
            # main_menu.enable()
        sprite_list = pg.sprite.groupcollide(monsters, bullets, True, True)
        for sprite in sprite_list:
            lose_enemy += 1
            new_enemy = Enemy('ufo.png', 80, 50,
            random.randint(30, cnst.HEIGHT_WINDOW - 30), random.randint(20, 30),
            random.randint(1, 3))
            monsters.add(new_enemy)
        if lose_enemy >= 10:
            finish = True
            window.blit(win, (200, 200))
        if reload_time:
            new_last_time = timer()
            if new_last_time - last_time < 3:
                reload_font = font.render('Reload...', 1, cnst.RED)
                window.blit(reload_font, (250, 460))
            else:
                num_fire = 0
                reload_time = False
        count = font.render(f'Счет: {lose_enemy}', 1, (255, 255, 255))
        lose = font.render(f'Пропущено: {enemy_finish}', 1, (255, 255, 255))
        window.blit(lose, (10, 50))
        window.blit(count, (10, 20))
    pg.display.update()
    clock.tick(cnst.FPS)
