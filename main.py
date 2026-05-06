import pygame
import random
import sys

# --- CONSTANTES ---
AMPLADA, ALÇADA = 800, 600
FPS = 60

# Colores (RGB)
VERD_FONS = (100, 255, 100)
VERMELL_FONS = (255, 100, 100)
BLAU_JUGADOR = (50, 50, 255)

class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vel = 5
        self.movent = False

    def actualitzar(self, tecles):
        self.movent = False
        # Movimiento con WASD o Flechas
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

class SistemaLlums:
    def __init__(self):
        self.estat = "VERD"
        self.ultim_canvi = pygame.time.get_ticks()
        self.interval = random.randint(2000, 4000) # Cambia cada 2-4 segundos

    def actualitzar(self):
        ara = pygame.time.get_ticks()
        if ara - self.ultim_canvi > self.interval:
            self.estat = "VERMELL" if self.estat == "VERD" else "VERD"
            self.ultim_canvi = ara
            self.interval = random.randint(1500, 3000)

    def get_color_fons(self):
        return VERD_FONS if self.estat == "VERD" else VERMELL_FONS

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((AMPLADA, ALÇADA))
    pygame.display.set_caption("Space Run - Prototip Fase 3")
    rellotge = pygame.time.Clock()

    jugador = Jugador(AMPLADA // 2, ALÇADA - 60)
    sistema_llums = SistemaLlums()

    corrent = True
    while corrent:
        # 1. GESTIÓN DE EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corrent = False

        # 2. LÓGICA DEL JUEGO
        tecles = pygame.key.get_pressed()
        jugador.actualitzar(tecles)
        sistema_llums.actualitzar()

        # Comprobar muerte (Prototipo: solo imprime por consola)
        if sistema_llums.estat == "VERMELL" and jugador.movent:
            print("¡Alerta! Te has movido en luz roja.")

        # 3. RENDERIZADO (DIBUJAR)
        pantalla.fill(sistema_llums.get_color_fons())
        jugador.dibuixar(pantalla)
        
        pygame.display.flip()
        rellotge.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()