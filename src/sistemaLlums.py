# src/sistemaLlums.py modificado
import pygame
import random

class SistemaLlums:
    def __init__(self):
        self.estat_actual = "VERD"
        self.nivel = 1
        self.intervalo_base = 5000  # ms para nivel 1 (5s)
        self.actualizar_intervalo()
        self.temps_canvi = pygame.time.get_ticks() + self.interval
        self.parpadeo = False
        self.timer_parpadeo = 0

    def actualizar_intervalo(self):
        # Nivel 1: entre 4 y 6 segundos (4000-6000)
        # Nivel 2: entre 2 y 4 segundos (2000-4000)
        # Nivel 3: entre 1 y 2 segundos (1000-2000)
        if self.nivel == 1:
            self.interval = random.randint(4000, 6000)
        elif self.nivel == 2:
            self.interval = random.randint(2000, 4000)
        else:  # nivel 3
            self.interval = random.randint(1000, 2000)

    def set_nivel(self, nivel):
        self.nivel = min(3, max(1, nivel))
        self.actualizar_intervalo()
        # Reiniciar el temporizador para evitar cambios inmediatos
        self.temps_canvi = pygame.time.get_ticks() + self.interval

    def actualitzar(self):
        ara = pygame.time.get_ticks()
        if ara >= self.temps_canvi:
            self.estat_actual = "VERMELL" if self.estat_actual == "VERD" else "VERD"
            self.actualizar_intervalo()
            self.temps_canvi = ara + self.interval
            self.parpadeo = True
            self.timer_parpadeo = ara

        if self.parpadeo and pygame.time.get_ticks() - self.timer_parpadeo > 100:
            self.parpadeo = False

    def get_estat(self):
        return self.estat_actual

    def get_color_fons(self):
        if self.parpadeo:
            return (255, 255, 255)
        if self.estat_actual == "VERD":
            return (20, 50, 20)
        else:
            return (50, 20, 20)