import pygame
import random
import sys

# --- CONSTANTS ---
AMPLADA, ALÇADA = 800, 600
FPS = 60

# Colors (RGB)
VERD_FONS = (100, 255, 100)
VERMELL_FONS = (255, 100, 100)
BLAU_JUGADOR = (50, 50, 255)
GROC_META = (255, 255, 0)
NEGRE = (0, 0, 0)
BLANC = (255, 255, 255)

class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vel = 5
        self.movent = False
        self.pos_inicial = (x, y) # Guardem la posició per quan reiniciem

    def actualitzar(self, tecles):
        self.movent = False
        # Moviment amb WASD o Fletxes
        if tecles[pygame.K_LEFT] or tecles[pygame.K_a]:
            self.rect.x -= self.vel
            self.movent = True
        if tecles[pygame.K_RIGHT] or tecles[pygame.K_d]:
            self.rect.x += self.vel
            self.movent = True
        if tecles[pygame.K_UP] or tecles[pygame.K_w]:
            self.rect.y -= self.vel
            self.movent = True
        if tecles[pygame.K_DOWN] or tecles[pygame.K_s]:
            self.rect.y += self.vel
            self.movent = True
            
        # Limitar a la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, AMPLADA, ALÇADA))

    def dibuixar(self, pantalla):
        pygame.draw.rect(pantalla, BLAU_JUGADOR, self.rect)
        
    def reiniciar(self):
        self.rect.x, self.rect.y = self.pos_inicial

class SistemaLlums:
    def __init__(self):
        self.estat = "VERD"
        self.ultim_canvi = pygame.time.get_ticks()
        self.interval = random.randint(2000, 4000)

    def actualitzar(self):
        ara = pygame.time.get_ticks()
        if ara - self.ultim_canvi > self.interval:
            self.estat = "VERMELL" if self.estat == "VERD" else "VERD"
            self.ultim_canvi = ara
            self.interval = random.randint(1500, 3000)

    def get_color_fons(self):
        return VERD_FONS if self.estat == "VERD" else VERMELL_FONS
        
    def reiniciar(self):
        self.estat = "VERD"
        self.ultim_canvi = pygame.time.get_ticks()

def dibuixar_text(pantalla, text, font, color, y_offset=0):
    """Funció auxiliar per centrar text a la pantalla fàcilment"""
    superficie = font.render