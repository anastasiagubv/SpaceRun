import pygame
import sys
from src.jugador import Jugador
from src.sistemaLlums import SistemaLlums

AMPLADA = 800
ALCADA = 600
META_X = 750

class GestorJoc:
    def __init__(self):
        self.temps_restant = 120.0
        self.estat_joc = "JUGANT"
        self.pantalla = None
        self.clock = None
        self.jugador = None
        self.llums = None

    def iniciar(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((AMPLADA, ALCADA))
        pygame.display.set_caption("Space Run")
        self.clock = pygame.time.Clock()
        
        # Instanciar el jugador a l'esquerra de la pantalla
        self.jugador = Jugador(50, ALCADA // 2 - 20)
        self.llums = SistemaLlums()

    def actualitzar_temps(self, dt):
        self.temps_restant -= dt
        if self.temps_restant <= 0:
            self.temps_restant = 0
            self.estat_joc = "PERDUT"

    def executar(self):
        self.iniciar()
        running = True
        font_gran = pygame.font.SysFont(None, 74)
        font_petita = pygame.font.SysFont(None, 36)

        while running:
            # Calculem el dt (segons transcorreguts des de l'últim frame)
            dt = self.clock.tick(60) / 1000.0 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if self.estat_joc == "JUGANT":
                # 1. Gestionar Input
                tecles = pygame.key.get_pressed()
                self.jugador.gestionar_input(tecles)
                
                # 2. Actualitzar lògica
                self.jugador.actualitzar(dt)
                self.llums.actualitzar()
                self.actualitzar_temps(dt)

                # 3. Comprovar Derrota (Moure's en vermell)
                if self.llums.get_estat() == "VERMELL" and self.jugador.esta_movent():
                    self.estat_joc = "PERDUT"
                    self.jugador.esta_viu = False

                # 4. Comprovar Victòria (Arribar a la meta)
                if self.jugador.x >= META_X - self.jugador.amplada:
                    self.estat_joc = "GUANYAT"

            # 5. Dibuixar a la pantalla
            self.dibuixar(font_gran, font_petita)

        pygame.quit()
        sys.exit()

    def dibuixar(self, font_gran, font_petita):
        # Dibuixar Fons
        self.pantalla.fill(self.llums.get_color_fons())

        # Dibuixar Meta (franja groga a la dreta)
        pygame.draw.rect(self.pantalla, (255, 255, 0), (META_X, 0, AMPLADA - META_X, ALCADA))

        # Dibuixar Jugador
        self.jugador.dibuixar(self.pantalla)

        # Dibuixar Temporitzador
        temps_text = font_petita.render(f"Temps: {int(self.temps_restant)}s", True, (0, 0, 0))
        self.pantalla.blit(temps_text, (10, 10))

        # Missatges de Final de Joc
        if self.estat_joc == "GUANYAT":
            text = font_gran.render("VICTÒRIA!", True, (0, 0, 255))
            self.pantalla.blit(text, (AMPLADA//2 - 120, ALCADA//2 - 30))
        elif self.estat_joc == "PERDUT":
            text = font_gran.render("GAME OVER", True, (0, 0, 0))
            self.pantalla.blit(text, (AMPLADA//2 - 150, ALCADA//2 - 30))

        pygame.display.flip()