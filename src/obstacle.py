import pygame
import random

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.vel_x = -100  # se mueven hacia la izquierda (opcional)
        self.color = (139, 69, 19)  # marrón

    def actualitzar(self, dt):
        # Opcional: mover hacia la izquierda
        self.rect.x += self.vel_x * dt
        # Si sale de la pantalla, reaparecer a la derecha con nueva Y
        if self.rect.x < -50:
            self.rect.x = 850
            self.rect.y = random.randint(20, 580 - 30)

    def dibuixar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, (50, 50, 50), self.rect, 2)