from random import randint, uniform
import numpy as np
import pygame.mouse
from planet import *
import sys

MAX_ACCELERATION = 0.01
MAX_SPEED = 4

pygame.init()
SX, SY = (1420, 680)


def clamp(n, x, y):
    if n < x:
        return x
    elif n > y:
        return y
    return n


FONT = pygame.font.SysFont('Roboto', 30)


def random_planet(x, pos=None, radii=None, make_mass_proportional=False):
    pos = pygame.Vector2(randint(0, SX), randint(0, SY)) if pos is None else pos
    radii = randint(10, 50) if not radii else radii
    for i in range(x):
        yield Planet(pos,
                     radius=radii,
                     mass=randint(1, 1) if not make_mass_proportional else radii / 16,
                     acceleration=pygame.Vector2(uniform(-0.2, 0.2) / 10000))


class Simulation:
    def __init__(self):
        self.planets: list[Planet] = list()
        self.screen = pygame.display.set_mode((SX, SY))
        pygame.display.set_caption("Planetas")
        self.states = {0: "Adicionar", 1: "Remover"}
        self.state = 0
        self.selected_size = 30

    def flip_state(self):
        self.state += 1
        if self.state not in self.states:
            self.state = 0

    def draw_text(self):
        render = FONT.render(self.states[self.state], False, pygame.color.Color('yellow'))
        self.screen.blit(render, (0, 0))
        render = FONT.render(f"Tamanho do Planeta: {self.selected_size}", False, pygame.color.Color('yellow'))
        self.screen.blit(render, (0, 30))

    def mainloop(self):
        click = False

        while True:
            self.screen.fill((0, 0, 0))
            self.draw_text()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.update_click()
                    click = True

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.flip_state()

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_u] and self.selected_size < 120:
                self.selected_size += 0.1

            elif pressed[pygame.K_y] and self.selected_size > 5:
                self.selected_size -= 0.1

            self.selected_size = round(self.selected_size, 2)

            # desenhando e atualizando os planetas
            for planet in list(self.planets):
                if not planet.exists:
                    del self.planets[self.planets.index(planet)]

                planet.blit(self.screen)
                planet.update(self.planets)
                planet.update_click(self.state, click)

            # desenhando o cursor
            pygame.draw.circle(self.screen, pygame.color.Color('blue'), pygame.mouse.get_pos(), self.selected_size)

            self.update()
            pygame.display.flip()

    def update_click(self):
        mouse_pos = pygame.mouse.get_pos()

        self.planets.extend(list(random_planet(1, pygame.Vector2(mouse_pos), radii=self.selected_size)))

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

                obj.velocity.x = clamp(obj.velocity.x, -MAX_SPEED, MAX_SPEED)
                obj.velocity.y = clamp(obj.velocity.y, -MAX_SPEED, MAX_SPEED)
