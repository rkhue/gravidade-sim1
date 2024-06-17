import pygame


class Planet:
    def __init__(self, pos: pygame.Vector2, radius=100, mass=10, velocity: pygame.Vector2 = None,
                 acceleration: pygame.Vector2 = None):
        self.pos = pos
        self.velocity = velocity if velocity else pygame.Vector2()
        self.acceleration = acceleration if acceleration else pygame.Vector2()
        self.radius = radius
        self.mass = mass

    def get_pos(self) -> pygame.Vector2:
        return self.pos

    def get_velocity(self) -> pygame.Vector2:
        return self.velocity

    def get_acceleration(self) -> pygame.Vector2:
        return self.acceleration

    def get_mass(self):
        return self.mass

    def get_radius(self):
        return self.radius

    def update(self):
        # primeiro atualizando a velocidade
        self.velocity += self.get_acceleration()
        # depois a posição
        self.pos += self.get_velocity()

    def blit(self, screen):
        pygame.draw.circle(screen, pygame.color.Color("red"), self.get_pos(), int(self.radius))
