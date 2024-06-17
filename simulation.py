from random import randint, uniform
import numpy as np
from planet import *
import sys

MAX_ACCELERATION = 10

pygame.init()
SX, SY = (1920, 1080)

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)


def random_planet(x):
    for i in range(x):
        yield Planet(pygame.Vector2(randint(0, SX), randint(0, SY)),
                     radius=randint(10, 100),
                     mass=randint(1, 1),
                     acceleration=pygame.Vector2(uniform(-1, 1) / 10000))


class Simulation:
    def __init__(self):
        self.planets: list[Planet] = list(random_planet(2))
        self.screen = pygame.display.set_mode((SX, SY))

    def mainloop(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # desenhando e atualizando os planetas
            for planet in self.planets:
                planet.blit(self.screen)
                planet.update(self.planets)

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

                obj.acceleration.x += clamp(obj.mass * ((bx - ox) * mag) * -1, -MAX_ACCELERATION, MAX_ACCELERATION)
                obj.acceleration.y += clamp(obj.mass * ((by - oy) * mag) * -1, -MAX_ACCELERATION, MAX_ACCELERATION)
