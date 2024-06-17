import pygame


class Planet:
    def __init__(self, pos: pygame.Vector2, color: pygame.Color = None,
                 radius=100, mass=10,
                 velocity: pygame.Vector2 = None,
                 acceleration: pygame.Vector2 = None):

        self.pos = pos
        self.velocity = velocity if velocity else pygame.Vector2()
        self.acceleration = acceleration if acceleration else pygame.Vector2()
        self.radius = radius
        self.color = pygame.color.Color("red") if color is None else color
        self.mass = mass
        self.frozen = False
        self.exists = True

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

    def get_color(self) -> pygame.Color:
        return self.color

    def update(self, others: list = None):
        if not self.frozen:
            self.update_collision(others)
            # primeiro atualizando a velocidade
            self.velocity += self.get_acceleration()
            # depois a posição
            self.pos += self.get_velocity()

    def update_click(self, state, click=False):
        mouse_pos = pygame.mouse.get_pos()

        if state == 1 and click:
            if (mouse_pos[0]-self.pos.x)**2 + (mouse_pos[1] - self.pos.y)**2 < self.radius**2:
                self.exists = False

    def update_collision(self, others: list | tuple = None):
        if not others:
            return

        for other in others:
            if other == self:
                continue

            distance = self.pos.distance_to(other.pos)
            if distance < self.radius + other.radius:
                self.freeze_self()
                other.freeze_self()

    def freeze_self(self):
        self.frozen = True
        self.color = pygame.color.Color("green")

    def blit(self, screen):
        pygame.draw.circle(screen, self.get_color(), self.get_pos(), int(self.radius))
