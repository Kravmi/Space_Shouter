#Создай собственный Шутер!
import pygame as pg
window = pg.display.set_mode((700, 500))
pg.display.set_caption("Space game")
game = True
background = pg.transform.scale(pg.image.load('galaxy.jpg'), (700, 500))
while game:
    window.blit(background, (0, 0))
    pg.display.update()