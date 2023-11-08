# Создай собственный Шутер!
import pygame as pg
import constants as cnst


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
        pass


window = pg.display.set_mode((cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW))
pg.display.set_caption("Space game")
game = True
finish = False
clock = pg.time.Clock()
background = pg.transform.scale(pg.image.load('galaxy.jpg'), \
    (cnst.WIDTH_WINDOW, cnst.HEIGHT_WINDOW))
pg.mixer.init()
pg.mixer.music.load('space.ogg')
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play()
player = Player('rocket.png', 80, 100, 5, 400, 10)
while game:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
    pg.display.update()
    clock.tick(cnst.FPS)
