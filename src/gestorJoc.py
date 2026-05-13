import pygame
import sys
import json
import os
import random
from src.jugador import Jugador
from src.sistemaLlums import SistemaLlums
from src.puntuacio import Puntuacio
from src.powerUp import PowerUp
from src.obstacle import Obstacle

AMPLADA = 800
ALCADA = 600
META_X = 700
FPS = 60

class GestorJoc:
    def __init__(self):
        self.temps_restant = 120.0
        self.estat_joc = "MENU"  # MENU, JUGANT, GUANYAT, PERDUT
        self.pantalla = None
        self.clock = None
        self.jugador = None
        self.llums = None
        self.puntuacio = None
        self.partides_jugades = 0
        self.record = 0
        self.top3 = []  # Lista de tuples (nom, punts)
        self.estelles = []
        self.powerups = []
        self.obstacles = []
        self.temps_proxim_powerup = 0
        self.nivel_actual = 1
        # Sonidos (cargar después de iniciar pygame)
        self.sonido_cambio = None
        self.sonido_muerte = None
        self.sonido_victoria = None
        self.sonido_powerup = None
        self.sonido_choque = None

    def cargar_record(self):
        try:
            if os.path.exists("record.json"):
                with open("record.json", "r") as f:
                    data = json.load(f)
                    self.record = data.get("puntuacio", 0)
                    self.top3 = data.get("top3", [])
            else:
                self.top3 = []
        except:
            self.top3 = []
        return self.record

    def guardar_record(self, puntuacio, nom_jugador="Jugador"):
        # Actualizar top 3
        self.top3.append((nom_jugador, puntuacio))
        self.top3.sort(key=lambda x: x[1], reverse=True)
        self.top3 = self.top3[:3]
        if puntuacio > self.record:
            self.record = puntuacio
        # Guardar en JSON
        try:
            with open("record.json", "w") as f:
                json.dump({"puntuacio": self.record, "top3": self.top3}, f)
        except:
            pass

    def cargar_sonidos(self):
        # Intentar cargar sonidos, si no existen, crear sonidos dummy (silencioso)
        try:
            self.sonido_cambio = pygame.mixer.Sound("sounds/cambio.wav")
            self.sonido_muerte = pygame.mixer.Sound("sounds/muerte.wav")
            self.sonido_victoria = pygame.mixer.Sound("sounds/victoria.wav")
            self.sonido_powerup = pygame.mixer.Sound("sounds/powerup.wav")
            self.sonido_choque = pygame.mixer.Sound("sounds/choque.wav")
        except:
            # Si no hay archivos, creamos sonidos simples con array (opcional)
            # Para evitar errores, asignamos None y luego verificamos antes de reproducir
            self.sonido_cambio = None
            self.sonido_muerte = None
            self.sonido_victoria = None
            self.sonido_powerup = None
            self.sonido_choque = None

    def reproducir_sonido(self, sonido):
        if sonido:
            sonido.play()

    def iniciar(self):
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((AMPLADA, ALCADA))
        pygame.display.set_caption("Space Run 🚀")
        self.clock = pygame.time.Clock()
        self.cargar_sonidos()
        self._crear_estelles()
        # Crear obstáculos fijos (3 asteroides en posiciones estratégicas)
        self.obstacles = [
            Obstacle(200, ALCADA//2 - 50, 30, 30),
            Obstacle(400, ALCADA//2 + 40, 35, 35),
            Obstacle(550, ALCADA//2 - 20, 25, 25)
        ]

    def _crear_estelles(self):
        import random
        self.estelles = []
        for _ in range(150):
            x = random.randint(0, AMPLADA)
            y = random.randint(0, ALCADA)
            vel = random.uniform(0.3, 1.5)
            size = random.randint(1, 3)
            self.estelles.append({"x": x, "y": y, "vel": vel, "size": size})

    def _actualitzar_estelles(self):
        for estella in self.estelles:
            estella["x"] -= estella["vel"]
            if estella["x"] < 0:
                estella["x"] = AMPLADA

    def _dibuixar_estelles(self):
        for estella in self.estelles:
            pygame.draw.circle(self.pantalla, (200, 200, 255), (int(estella["x"]), int(estella["y"])), estella["size"])

    def nova_partida(self, nom_jugador="Jugador"):
        self.temps_restant = 120.0
        self.estat_joc = "JUGANT"
        self.jugador = Jugador(50, ALCADA // 2 - 20)
        self.llums = SistemaLlums()
        self.puntuacio = Puntuacio(self.jugador)
        self.partides_jugades += 1
        self.powerups = []
        self.temps_proxim_powerup = pygame.time.get_ticks() + 5000  # primer powerup a los 5 seg
        self.nivel_actual = 1
        self.llums.set_nivel(1)
        self.nom_jugador = nom_jugador
        self.obstacles.clear()
        self.powerups.clear()
        for _ in range(3):
            x = random.randint(400, 800)
            y = random.randint(20, 580 - 30)
            self.obstacles.append(Obstacle(x, y))

    def actualitzar_temps(self, dt):
        self.temps_restant -= dt
        if self.temps_restant <= 0:
            self.temps_restant = 0
            self.estat_joc = "PERDUT"
            self.reproducir_sonido(self.sonido_muerte)

    def actualitzar_dificultat_per_nivell(self):
        # Subir de nivel cada 300 puntos
        punts = self.puntuacio.get_punts()
        nuevo_nivel = 1
        if punts >= 600:
            nuevo_nivel = 3
        elif punts >= 300:
            nuevo_nivel = 2
        if nuevo_nivel != self.nivel_actual:
            self.nivel_actual = nuevo_nivel
            self.llums.set_nivel(self.nivel_actual)
            # Opcional: reproducir sonido de cambio de nivel
            self.reproducir_sonido(self.sonido_cambio)

    def generar_powerup(self):
        # Generar powerup en una posición aleatoria (evitar la meta y bordes)
        x = random.randint(50, META_X - 50)
        y = random.randint(50, ALCADA - 50)
        # Elegir tipo aleatorio
        tipus = random.choice(["punts", "temps", "escut"])
        self.powerups.append(PowerUp(x, y, tipus))

    def aplicar_powerup(self, powerup):
        if powerup.tipus == "punts":
            self.puntuacio.punts += 50
        elif powerup.tipus == "temps":
            self.temps_restant += 5
            if self.temps_restant > 120:
                self.temps_restant = 120
        elif powerup.tipus == "escut":
            self.jugador.aplicar_escudo()
        self.reproducir_sonido(self.sonido_powerup)

    def executar(self):
        self.iniciar()
        running = True
        font_gran = pygame.font.SysFont(None, 74)
        font_mitjana = pygame.font.SysFont(None, 48)
        font_petita = pygame.font.SysFont(None, 32)
        font_xica = pygame.font.SysFont(None, 24)

        # Solicitar nombre al inicio (simplificado, usamos input en consola)
        nom = input("Introdueix el teu nom per al rànquing: ") or "Jugador"

        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.estat_joc == "MENU" and event.key == pygame.K_SPACE:
                        self.nova_partida(nom)
                    elif self.estat_joc == "PERDUT" and event.key == pygame.K_r:
                        self.nova_partida(nom)
                    elif self.estat_joc == "GUANYAT" and event.key == pygame.K_r:
                        self.nova_partida(nom)

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
        tecles = pygame.key.get_pressed()
        self.jugador.gestionar_input(tecles)
        self.jugador.actualitzar(dt)
        self.llums.actualitzar()
        self.puntuacio.actualitzar(dt)
        self.actualitzar_temps(dt)
        self.actualitzar_dificultat_per_nivell()  # subir nivel por puntos
        self._actualitzar_estelles()

        # Generar power-ups periódicamente
        ara = pygame.time.get_ticks()
        if ara >= self.temps_proxim_powerup and len(self.powerups) < 3:
            self.generar_powerup()
            self.temps_proxim_powerup = ara + random.randint(8000, 15000)

        # Colisiones con power-ups
        for powerup in self.powerups[:]:
            if self.jugador.x < powerup.rect.x + powerup.rect.width and \
               self.jugador.x + self.jugador.amplada > powerup.rect.x and \
               self.jugador.y < powerup.rect.y + powerup.rect.height and \
               self.jugador.y + self.jugador.alcada > powerup.rect.y:
                self.aplicar_powerup(powerup)
                self.powerups.remove(powerup)

        # Colisiones con obstáculos (asteroides)
        for obs in self.obstacles:
            if self.jugador.x < obs.rect.x + obs.rect.width and \
               self.jugador.x + self.jugador.amplada > obs.rect.x and \
               self.jugador.y < obs.rect.y + obs.rect.height and \
               self.jugador.y + self.jugador.alcada > obs.rect.y:
                # Penalización: perder 10 puntos y retroceder un poco
                self.puntuacio.punts = max(0, self.puntuacio.punts - 10)
                self.jugador.x = max(0, self.jugador.x - 40)
                self.reproducir_sonido(self.sonido_choque)

        # Comprobar muerte (movimiento en luz roja)
        if self.llums.get_estat() == "VERMELL" and self.jugador.esta_movent():
            if self.jugador.tiene_escudo:
                self.jugador.perder_escudo()
                # No muere, pero pierde el escudo
                self.reproducir_sonido(self.sonido_choque)
            else:
                self.estat_joc = "PERDUT"
                self.jugador.esta_viu = False
                self.reproducir_sonido(self.sonido_muerte)
                self.guardar_record(self.puntuacio.get_punts(), self.nom_jugador)

        # Comprobar victoria
        if self.jugador.x >= META_X - self.jugador.amplada:
            self.puntuacio.bonus_final(self.temps_restant)
            self.estat_joc = "GUANYAT"
            self.reproducir_sonido(self.sonido_victoria)
            self.guardar_record(self.puntuacio.get_punts(), self.nom_jugador)
            
        # Generar nuevos obstáculos cada cierto tiempo
        self.timer_generacio_obstacle += dt
        if self.timer_generacio_obstacle > 4.0:  # cada 4 segundos
            self.timer_generacio_obstacle = 0
            if len(self.obstacles) < 5:
                self.obstacles.append(Obstacle(850, random.randint(20, 580 - 30)))

        # Actualizar obstáculos
        for obs in self.obstacles[:]:
            obs.actualitzar(dt)
            if obs.rect.x < -50:
                self.obstacles.remove(obs)

        # Generar power-ups
        self.timer_generacio_powerup += dt
        if self.timer_generacio_powerup > 8.0 and len(self.powerups) < 3:
            self.timer_generacio_powerup = 0
            tipus = random.choice(["punts", "temps", "escut"])
            self.powerups.append(PowerUp(850, random.randint(20, 580 - 20), tipus))

        # Actualizar power-ups
        for pw in self.powerups[:]:
            if not pw.actualitzar(dt):
                self.powerups.remove(pw)

        # Colisiones con obstáculos
        for obs in self.obstacles:
            if self.jugador.rect.colliderect(obs.rect):
                self.puntuacio.punts = max(0, self.puntuacio.punts - 10)
                # Retroceder un poco
                self.jugador.x = max(0, self.jugador.x - 50)
                self.reproduir_so("choque")
                # Eliminar ese obstáculo
                self.obstacles.remove(obs)
                break

        # Colisiones con power-ups
        for pw in self.powerups[:]:
            if self.jugador.rect.colliderect(pw.rect):
                if pw.tipus == "punts":
                    self.puntuacio.punts += 50
                elif pw.tipus == "temps":
                    self.temps_restant = min(120, self.temps_restant + 5)
                elif pw.tipus == "escut":
                    self.jugador.tiene_escudo = True
                self.reproduir_so("powerup")
                self.powerups.remove(pw)

    def _dibuixar_menu(self, font_gran, font_mitjana, font_petita, font_xica):
        self.pantalla.fill((10, 10, 30))
        self._dibuixar_estelles()
        title = font_gran.render("SPACE RUN", True, (100, 200, 255))
        self.pantalla.blit(title, (AMPLADA//2 - 180, 80))
        subtitle = font_mitjana.render("🚀 Reacció Ràpida 🚀", True, (150, 200, 255))
        self.pantalla.blit(subtitle, (AMPLADA//2 - 160, 160))

        instr1 = font_petita.render("Creua el passadís fins a la meta", True, (200,200,200))
        instr2 = font_petita.render("🟢 Llum VERDA: pots avançar", True, (100,255,100))
        instr3 = font_petita.render("🔴 Llum VERMELLA: atura't completament!", True, (255,100,100))
        instr4 = font_petita.render("⏱️  Tens 120 segons", True, (200,200,200))
        self.pantalla.blit(instr1, (AMPLADA//2 - 180, 260))
        self.pantalla.blit(instr2, (AMPLADA//2 - 160, 310))
        self.pantalla.blit(instr3, (AMPLADA//2 - 210, 360))
        self.pantalla.blit(instr4, (AMPLADA//2 - 120, 410))

        # Mostrar top 3
        y_offset = 460
        top_title = font_petita.render("🏆 TOP 3 🏆", True, (255,215,0))
        self.pantalla.blit(top_title, (AMPLADA//2 - 70, y_offset))
        y_offset += 30
        for i, (nom, punts) in enumerate(self.top3):
            texto = font_xica.render(f"{i+1}. {nom}: {punts}", True, (255,255,200))
            self.pantalla.blit(texto, (AMPLADA//2 - 100, y_offset + i*25))

        # Start
        start_text = font_mitjana.render("Pressiona SPACE per jugar", True, (100,255,100))
        self.pantalla.blit(start_text, (AMPLADA//2 - 200, 540))

    def _dibuixar_partida(self, font_gran, font_petita, font_xica):
        self.pantalla.fill(self.llums.get_color_fons())
        self._dibuixar_estelles()
        # Meta
        pygame.draw.rect(self.pantalla, (255, 255, 0), (META_X, 0, AMPLADA - META_X, ALCADA))
        # Obstáculos
        for obs in self.obstacles:
            obs.dibuixar(self.pantalla)
        # Power-ups
        for p in self.powerups:
            p.dibuixar(self.pantalla)
        # Barra de progreso
        self._dibuixar_barra_progres(font_xica)
        self.jugador.dibuixar(self.pantalla)

        # Información UI
        luz_color = (100,255,100) if self.llums.get_estat() == "VERD" else (255,100,100)
        luz_texto = "VERD" if self.llums.get_estat() == "VERD" else "VERMELL"
        luz = font_xica.render(f"Llum: {luz_texto}", True, luz_color)
        self.pantalla.blit(luz, (AMPLADA - 200, 10))
        temps_text = font_petita.render(f"Temps: {int(self.temps_restant)}s", True, (0,0,0))
        self.pantalla.blit(temps_text, (10, 10))
        punts_text = font_petita.render(f"Punts: {self.puntuacio.get_punts()}", True, (0,0,0))
        self.pantalla.blit(punts_text, (10, 50))
        nivell_text = font_petita.render(f"Nivell: {self.nivel_actual}", True, (0,0,0))
        self.pantalla.blit(nivell_text, (10, 90))
        if self.jugador.tiene_escudo:
            escudo_text = font_xica.render("🛡️ Escudo activo", True, (0,255,0))
            self.pantalla.blit(escudo_text, (10, 130))

    def _dibuixar_barra_progres(self, font_xica):
        bar_width = AMPLADA - 40
        bar_height = 20
        bar_x = 20
        bar_y = ALCADA - 30
        pygame.draw.rect(self.pantalla, (100,100,100), (bar_x, bar_y, bar_width, bar_height))
        progreso = (self.jugador.x / META_X) * bar_width
        pygame.draw.rect(self.pantalla, (100,200,255), (bar_x, bar_y, progreso, bar_height))
        pygame.draw.rect(self.pantalla, (200,200,200), (bar_x, bar_y, bar_width, bar_height), 2)

    def _dibuixar_victòria(self, font_gran, font_mitjana, font_petita, font_xica):
        self.pantalla.fill((30,60,30))
        self._dibuixar_estelles()
        victoria = font_gran.render("¡VICTÒRIA!", True, (100,255,100))
        self.pantalla.blit(victoria, (AMPLADA//2 - 150, 80))
        punts = self.puntuacio.get_punts()
        punts_text = font_mitjana.render(f"Punts finals: {punts}", True, (150,255,150))
        self.pantalla.blit(punts_text, (AMPLADA//2 - 180, 200))
        if punts > self.record:
            record_text = font_petita.render("🏆 NOU RECORD!", True, (255,215,0))
        else:
            record_text = font_petita.render(f"Record: {self.record}", True, (200,200,200))
        self.pantalla.blit(record_text, (AMPLADA//2 - 140, 280))
        restart = font_petita.render("Pressiona R per jugar de nou", True, (200,255,200))
        self.pantalla.blit(restart, (AMPLADA//2 - 180, 420))

    def _dibuixar_game_over(self, font_gran, font_mitjana, font_petita, font_xica):
        self.pantalla.fill((60,30,30))
        self._dibuixar_estelles()
        game_over = font_gran.render("GAME OVER", True, (255,100,100))
        self.pantalla.blit(game_over, (AMPLADA//2 - 180, 80))
        punts = self.puntuacio.get_punts()
        punts_text = font_mitjana.render(f"Punts: {punts}", True, (255,150,150))
        self.pantalla.blit(punts_text, (AMPLADA//2 - 120, 200))
        if self.temps_restant <= 0:
            motiu = font_petita.render("Se t'ha acabat el temps!", True, (255,150,150))
        else:
            motiu = font_petita.render("T'has mogut en llum vermella!", True, (255,150,150))
        self.pantalla.blit(motiu, (AMPLADA//2 - 180, 300))
        record_text = font_xica.render(f"Record: {self.record}", True, (200,200,200))
        self.pantalla.blit(record_text, (AMPLADA//2 - 130, 360))
        restart = font_petita.render("Pressiona R per jugar de nou", True, (200,200,200))
        self.pantalla.blit(restart, (AMPLADA//2 - 180, 440))
                
        def reproduir_so(self, nom):
            if nom in self.sons and self.sons[nom]:
                self.sons[nom].play()