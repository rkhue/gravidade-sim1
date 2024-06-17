from random import randint
import numpy as np
from planet import *
import sys

pygame.init()
SX, SY = (1920, 1080)


class Simulation:
    def __init__(self):
        self.planets: list[Planet] = [Planet(pygame.Vector2(randint(0, SX), randint(0, SY))) for _ in range(2)]
        self.screen = pygame.display.set_mode((SX, SY))

    def mainloop(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.key == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # desenhando os planetas
            for planet in self.planets:
                planet.blit(self.screen)
            self.update()
            pygame.display.flip()

    def update(self):
        for obj in self.planets:
            for other in self.planets:
                if other == obj:
                    continue
                bx, by = obj.pos.x, obj.pos.y
                ox, oy = other.pos.x, other.pos.y

                mag = 1. / np.sqrt((ox - bx) ** 2 + (oy - by) ** 2) ** 3

                obj.acceleration.x += obj.mass * ((bx - ox) * mag) * -1
                obj.acceleration.y += obj.mass * ((by - oy) * mag) * -1
