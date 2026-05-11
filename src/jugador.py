import pygame
import math

class Jugador:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vel_x = 0.0
        self.esta_viu = True
        self.amplada = 40
        self.alcada = 40
        self.velocitat_base = 300  # Píxels per segon
        self.parpelleja_timer = 0  # Para el efecto de parpadeo
        self.visible = True  # Para la animación de parpadeo

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
        
        # Evitar que surti per la dreta
        if self.x > 800 - self.amplada:
            self.x = 800 - self.amplada
        
        # Actualizar animación de parpadeo si está muerto
        if not self.esta_viu:
            self.parpelleja_timer += dt
            # Parpadea cada 0.15 segundos
            if self.parpelleja_timer > 0.15:
                self.visible = not self.visible
                self.parpelleja_timer = 0

    def esta_movent(self):
        # Retorna True si la velocitat no és zero
        return self.vel_x != 0

    def dibuixar(self, pantalla):
        # No dibujar si está en animación de parpadeo y no es visible
        if not self.esta_viu and not self.visible:
            return
        
        rect = pygame.Rect(self.x, self.y, self.amplada, self.alcada)
        
        if self.esta_viu:
            # Jugador normal: azul
            pygame.draw.rect(pantalla, (50, 50, 255), rect)
            # Borde más claro
            pygame.draw.rect(pantalla, (100, 150, 255), rect, 3)
            
            # Ojos del jugador
            pygame.draw.circle(pantalla, (255, 255, 255), 
                             (int(self.x + 15), int(self.y + 15)), 5)
            pygame.draw.circle(pantalla, (255, 255, 255), 
                             (int(self.x + 25), int(self.y + 15)), 5)
            pygame.draw.circle(pantalla, (50, 50, 255), 
                             (int(self.x + 15), int(self.y + 15)), 3)
            pygame.draw.circle(pantalla, (50, 50, 255), 
                             (int(self.x + 25), int(self.y + 15)), 3)
        else:
            # Jugador muerto: rojo oscuro parpadeante
            pygame.draw.rect(pantalla, (150, 50, 50), rect)
            pygame.draw.rect(pantalla, (255, 100, 100), rect, 3)
            
            # Cruz en lugar de ojos
            pygame.draw.line(pantalla, (255, 255, 255), 
                           (int(self.x + 10), int(self.y + 10)), 
                           (int(self.x + 20), int(self.y + 20)), 2)
            pygame.draw.line(pantalla, (255, 255, 255), 
                           (int(self.x + 20), int(self.y + 10)), 
                           (int(self.x + 10), int(self.y + 20)), 2)