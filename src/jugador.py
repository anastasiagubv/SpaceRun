import pygame

class Jugador:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vel_x = 0.0
        self.esta_viu = True
        self.amplada = 40
        self.alcada = 40
        self.velocitat_base = 300 # Píxels per segon

    def gestionar_input(self, tecles):
        self.vel_x = 0.0
        # Moviment només horitzontal (cap a la meta)
        if tecles[pygame.K_RIGHT] or tecles[pygame.K_d]:
            self.vel_x = self.velocitat_base
        elif tecles[pygame.K_LEFT] or tecles[pygame.K_a]:
            self.vel_x = -self.velocitat_base

    def actualitzar(self, dt):
        # Movem el jugador multiplicant per dt (delta time)
        self.x += self.vel_x * dt
        
        # Evitar que surti per l'esquerra de la pantalla
        if self.x < 0:
            self.x = 0

    def esta_movent(self):
        # Retorna True si la velocitat no és zero
        return self.vel_x != 0

    def dibuixar(self, pantalla):
        rect = pygame.Rect(self.x, self.y, self.amplada, self.alcada)
        pygame.draw.rect(pantalla, (50, 50, 255), rect) # Blau