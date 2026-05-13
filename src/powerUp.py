import pygame
import random

class PowerUp:
    def __init__(self, x, y, tipus):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.tipus = tipus  # "punts", "temps", "escut"
        self.color = {"punts": (255, 255, 0), "temps": (0, 255, 255), "escut": (0, 255, 0)}[tipus]
        self.vel_x = -80  # se mueve hacia la izquierda

    def actualitzar(self, dt):
        self.rect.x += self.vel_x * dt
        if self.rect.x < -30:
            return False  # eliminarlo
        return True

    def dibuixar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, (255, 255, 255), self.rect, 2)