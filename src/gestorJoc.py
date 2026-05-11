import pygame
import sys
import json
import os
from src.jugador import Jugador
from src.sistemaLlums import SistemaLlums
from src.puntuacio import Puntuacio

AMPLADA = 800
ALCADA = 600
META_X = 700
FPS = 60

class GestorJoc:
    def __init__(self):
        self.temps_restant = 120.0
        self.estat_joc = "MENU"  # Estados: MENU, JUGANT, GUANYAT, PERDUT
        self.pantalla = None
        self.clock = None
        self.jugador = None
        self.llums = None
        self.puntuacio = None
        self.partides_jugades = 0
        self.record = self.cargar_record()
        self.estelles = []  # Para parallax effect

    def iniciar(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((AMPLADA, ALCADA))
        pygame.display.set_caption("Space Run 🚀")
        self.clock = pygame.time.Clock()
        self._crear_estelles()

    def _crear_estelles(self):
        """Crea estrellas para el efecto parallax"""
        import random
        self.estelles = []
        for _ in range(100):
            x = random.randint(0, AMPLADA)
            y = random.randint(0, ALCADA)
            velocitat = random.uniform(0.5, 2.0)
            tamany = random.randint(1, 3)
            self.estelles.append({"x": x, "y": y, "vel": velocitat, "size": tamany})

    def _actualitzar_estelles(self):
        """Actualiza la posición de las estrellas (parallax)"""
        for estella in self.estelles:
            estella["x"] -= estella["vel"]
            if estella["x"] < 0:
                estella["x"] = AMPLADA

    def _dibuixar_estelles(self):
        """Dibuja las estrellas de fondo"""
        for estella in self.estelles:
            pygame.draw.circle(self.pantalla, (200, 200, 255), 
                             (int(estella["x"]), int(estella["y"])), estella["size"])

    def nova_partida(self):
        """Inicializa una nueva partida"""
        self.temps_restant = 120.0
        self.estat_joc = "JUGANT"
        self.jugador = Jugador(50, ALCADA // 2 - 20)
        self.llums = SistemaLlums()
        self.puntuacio = Puntuacio(self.jugador)
        self.partides_jugades += 1

    def actualitzar_temps(self, dt):
        self.temps_restant -= dt
        if self.temps_restant <= 0:
            self.temps_restant = 0
            self.estat_joc = "PERDUT"

    def cargar_record(self):
        """Carga el mejor record de un fichero JSON"""
        try:
            if os.path.exists("record.json"):
                with open("record.json", "r") as f:
                    data = json.load(f)
                    return data.get("puntuacio", 0)
        except:
            pass
        return 0

    def guardar_record(self, puntuacio):
        """Guarda el record si es mejor que el anterior"""
        if puntuacio > self.record:
            self.record = puntuacio
            try:
                with open("record.json", "w") as f:
                    json.dump({"puntuacio": self.record}, f)
            except:
                pass

    def executar(self):
        self.iniciar()
        running = True
        font_gran = pygame.font.SysFont(None, 74)
        font_mitjana = pygame.font.SysFont(None, 48)
        font_petita = pygame.font.SysFont(None, 32)
        font_xica = pygame.font.SysFont(None, 24)

        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.estat_joc == "MENU" and event.key == pygame.K_SPACE:
                        self.nova_partida()
                    elif self.estat_joc == "PERDUT" and event.key == pygame.K_r:
                        self.nova_partida()
                    elif self.estat_joc == "GUANYAT" and event.key == pygame.K_r:
                        self.nova_partida()

            if self.estat_joc == "MENU":
                self._dibuixar_menu(font_gran, font_mitjana, font_petita, font_xica)
            elif self.estat_joc == "JUGANT":
                self._actualitzar_partida(dt, font_petita, font_xica)
                self._dibuixar_partida(font_gran, font_petita, font_xica)
            elif self.estat_joc == "GUANYAT":
                self._dibuixar_victòria(font_gran, font_mitjana, font_petita, font_xica)
            elif self.estat_joc == "PERDUT":
                self._dibuixar_game_over(font_gran, font_mitjana, font_petita, font_xica)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _actualitzar_partida(self, dt, font_petita, font_xica):
        """Actualiza la lógica de una partida en curso"""
        tecles = pygame.key.get_pressed()
        self.jugador.gestionar_input(tecles)
        
        self.jugador.actualitzar(dt)
        self.llums.actualitzar()
        self.puntuacio.actualitzar(dt)
        self.actualitzar_temps(dt)
        self._actualitzar_estelles()

        # Comprobar muerte (movimiento en luz roja)
        if self.llums.get_estat() == "VERMELL" and self.jugador.esta_movent():
            self.estat_joc = "PERDUT"
            self.jugador.esta_viu = False
            self.guardar_record(self.puntuacio.get_punts())

        # Comprobar victoria
        if self.jugador.x >= META_X - self.jugador.amplada:
            self.estat_joc = "GUANYAT"
            self.guardar_record(self.puntuacio.get_punts())

    def _dibuixar_menu(self, font_gran, font_mitjana, font_petita, font_xica):
        """Dibuja la pantalla del menú inicial"""
        # Fondo con gradiente simulado
        self.pantalla.fill((10, 10, 30))
        self._dibuixar_estelles()

        # Título
        title = font_gran.render("SPACE RUN", True, (100, 200, 255))
        self.pantalla.blit(title, (AMPLADA//2 - 180, 80))

        # Subtítulo
        subtitle = font_mitjana.render("🚀 Reacció Ràpida 🚀", True, (150, 200, 255))
        self.pantalla.blit(subtitle, (AMPLADA//2 - 160, 160))

        # Instrucciones
        instr1 = font_petita.render("Creua el passadís fins a la meta", True, (200, 200, 200))
        instr2 = font_petita.render("🟢 Llum VERDA: pots avançar", True, (100, 255, 100))
        instr3 = font_petita.render("🔴 Llum VERMELLA: atura't completament!", True, (255, 100, 100))
        instr4 = font_petita.render("⏱️  Tens 120 segons", True, (200, 200, 200))

        self.pantalla.blit(instr1, (AMPLADA//2 - 180, 260))
        self.pantalla.blit(instr2, (AMPLADA//2 - 160, 310))
        self.pantalla.blit(instr3, (AMPLADA//2 - 210, 360))
        self.pantalla.blit(instr4, (AMPLADA//2 - 120, 410))

        # Record
        record_text = font_xica.render(f"🏆 Millor puntuació: {self.record}", True, (255, 215, 0))
        self.pantalla.blit(record_text, (AMPLADA//2 - 150, 460))

        # Start button
        start_text = font_mitjana.render("Pressiona SPACE per jugar", True, (100, 255, 100))
        self.pantalla.blit(start_text, (AMPLADA//2 - 200, 520))

    def _dibuixar_partida(self, font_gran, font_petita, font_xica):
        """Dibuja la partida en curso"""
        # Fondo con color según luz
        self.pantalla.fill(self.llums.get_color_fons())
        self._dibuixar_estelles()

        # Meta (franja groga)
        pygame.draw.rect(self.pantalla, (255, 255, 0), (META_X, 0, AMPLADA - META_X, ALCADA))

        # Barra de progres
        self._dibuixar_barra_progres(font_xica)

        # Jugador
        self.jugador.dibuixar(self.pantalla)

        # Luz indicador
        luz_color = (100, 255, 100) if self.llums.get_estat() == "VERD" else (255, 100, 100)
        luz_texto = "VERD" if self.llums.get_estat() == "VERD" else "VERMELL"
        luz = font_xica.render(f"Llum: {luz_texto}", True, luz_color)
        self.pantalla.blit(luz, (AMPLADA - 200, 10))

        # Tiempo
        temps_text = font_petita.render(f"Temps: {int(self.temps_restant)}s", True, (0, 0, 0))
        self.pantalla.blit(temps_text, (10, 10))

        # Puntuación
        punts_text = font_petita.render(f"Punts: {self.puntuacio.get_punts()}", True, (0, 0, 0))
        self.pantalla.blit(punts_text, (10, 50))

    def _dibuixar_barra_progres(self, font_xica):
        """Dibuja una barra de progreso visual"""
        bar_width = AMPLADA - 40
        bar_height = 20
        bar_x = 20
        bar_y = ALCADA - 30

        # Fondo
        pygame.draw.rect(self.pantalla, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        # Progreso
        progreso = (self.jugador.x / META_X) * bar_width
        pygame.draw.rect(self.pantalla, (100, 200, 255), (bar_x, bar_y, progreso, bar_height))

        # Borde
        pygame.draw.rect(self.pantalla, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)

    def _dibuixar_victòria(self, font_gran, font_mitjana, font_petita, font_xica):
        """Dibuja la pantalla de victoria"""
        self.pantalla.fill((30, 60, 30))
        self._dibuixar_estelles()

        # Mensaje de victoria
        victoria = font_gran.render("¡VICTÒRIA!", True, (100, 255, 100))
        self.pantalla.blit(victoria, (AMPLADA//2 - 150, 80))

        # Puntuación
        punts = self.puntuacio.get_punts()
        punts_text = font_mitjana.render(f"Punts finals: {punts}", True, (150, 255, 150))
        self.pantalla.blit(punts_text, (AMPLADA//2 - 180, 200))

        # Record
        if punts > self.record:
            record_text = font_petita.render("🏆 NOU RECORD!", True, (255, 215, 0))
        else:
            record_text = font_petita.render(f"Record: {self.record}", True, (200, 200, 200))
        self.pantalla.blit(record_text, (AMPLADA//2 - 140, 280))

        # Reiniciar
        restart = font_petita.render("Pressiona R per jugar de nou", True, (200, 255, 200))
        self.pantalla.blit(restart, (AMPLADA//2 - 180, 420))

    def _dibuixar_game_over(self, font_gran, font_mitjana, font_petita, font_xica):
        """Dibuja la pantalla de game over"""
        self.pantalla.fill((60, 30, 30))
        self._dibuixar_estelles()

        # Mensaje
        game_over = font_gran.render("GAME OVER", True, (255, 100, 100))
        self.pantalla.blit(game_over, (AMPLADA//2 - 180, 80))

        # Puntuación
        punts = self.puntuacio.get_punts()
        punts_text = font_mitjana.render(f"Punts: {punts}", True, (255, 150, 150))
        self.pantalla.blit(punts_text, (AMPLADA//2 - 120, 200))

        # Motivo
        if self.temps_restant <= 0:
            motiu = font_petita.render("Se t'ha acabat el temps!", True, (255, 150, 150))
        else:
            motiu = font_petita.render("T'has mogut en llum vermella!", True, (255, 150, 150))
        self.pantalla.blit(motiu, (AMPLADA//2 - 180, 300))

        # Record
        record_text = font_xica.render(f"Record: {self.record}", True, (200, 200, 200))
        self.pantalla.blit(record_text, (AMPLADA//2 - 130, 360))

        # Reiniciar
        restart = font_petita.render("Pressiona R per jugar de nou", True, (200, 200, 200))
        self.pantalla.blit(restart, (AMPLADA//2 - 180, 440))