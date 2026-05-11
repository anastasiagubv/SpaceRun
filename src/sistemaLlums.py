import pygame
import random

class SistemaLlums:
    def __init__(self):
        self.estat_actual = "VERD"
        self.interval = random.randint(2000, 5000)
        self.temps_canvi = pygame.time.get_ticks() + self.interval

    def actualitzar(self):
        ara = pygame.time.get_ticks()
        # Si el temps actual supera el temps previst per al canvi
        if ara >= self.temps_canvi:
            # Alternem l'estat
            if self.estat_actual == "VERD":
                self.estat_actual = "VERMELL"
            else:
                self.estat_actual = "VERD"
            
            # Calculem el pròxim canvi
            self.interval = random.randint(2000, 5000)
            self.temps_canvi = ara + self.interval

    def get_estat(self):
        return self.estat_actual

    def get_color_fons(self):
        if self.estat_actual == "VERD":
            return (40, 80, 40)  # Verd fosc més atmosfèric
        else:
            return (80, 40, 40)  # Vermell fosc més atmosfèric