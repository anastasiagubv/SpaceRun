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
ALCADA  = 600
META_X  = 720
FPS     = 60


class GestorJoc:
    """Controlador central del joc Space Run."""

    def __init__(self):
        # Estat principal
        self.estat_joc = "NOM_INPUT"   # NOM_INPUT → MENU → JUGANT → GUANYAT/PERDUT
        self.pantalla  = None
        self.clock     = None

        # Entitats del joc
        self.jugador  = None
        self.llums    = None
        self.puntuacio = None
        self.obstacles = []
        self.powerups  = []

        # Temps i puntuació
        self.temps_restant = 120.0
        self.record = 0
        self.top3   = []
        self.nom_jugador = ""

        # Efecte de fons d'estelles
        self.estelles = []

        # Timers de generació d'objectes
        self.timer_obstacle = 0.0
        self.timer_powerup  = 0.0

        # Nivell de dificultat
        self.nivel_actual = 1

        # Sonidos (s'inicialitzen al prémer Play)
        self.sonido_cambio   = None
        self.sonido_muerte   = None
        self.sonido_victoria = None
        self.sonido_powerup  = None
        self.sonido_choque   = None

    # ==================================================================
    # INICIALITZACIÓ
    # ==================================================================
    def iniciar(self):
        """Inicialitza pygame, la finestra i els recursos compartits."""
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((AMPLADA, ALCADA))
        pygame.display.set_caption("Space Run 🚀")
        self.clock = pygame.time.Clock()
        self._crear_estelles()
        self._carregar_sonidos()
        self.cargar_record()

    def _carregar_sonidos(self):
        """Carrega els fitxers de so. Si no existeixen, els deixa a None."""
        arxius = {
            "cambio":   "sounds/cambio.wav",
            "muerte":   "sounds/muerte.wav",
            "victoria": "sounds/victoria.wav",
            "powerup":  "sounds/powerup.wav",
            "choque":   "sounds/choque.wav",
        }
        for clau, ruta in arxius.items():
            try:
                so = pygame.mixer.Sound(ruta)
                setattr(self, f"sonido_{clau}", so)
            except Exception:
                setattr(self, f"sonido_{clau}", None)

    def _reproduir_so(self, so):
        """Reprodueix un so si està disponible."""
        if so:
            so.play()

    # ==================================================================
    # ESTRELLES (fons parallax)
    # ==================================================================
    def _crear_estelles(self):
        self.estelles = [
            {
                "x":   random.randint(0, AMPLADA),
                "y":   random.randint(0, ALCADA),
                "vel": random.uniform(0.3, 1.5),
                "size": random.randint(1, 3),
            }
            for _ in range(150)
        ]

    def _actualitzar_estelles(self):
        for e in self.estelles:
            e["x"] -= e["vel"]
            if e["x"] < 0:
                e["x"] = AMPLADA

    def _dibuixar_estelles(self):
        for e in self.estelles:
            pygame.draw.circle(
                self.pantalla, (200, 200, 255),
                (int(e["x"]), int(e["y"])), e["size"]
            )

    # ==================================================================
    # RECORDS
    # ==================================================================
    def cargar_record(self):
        try:
            if os.path.exists("record.json"):
                with open("record.json", "r") as f:
                    data = json.load(f)
                    self.record = data.get("puntuacio", 0)
                    self.top3   = data.get("top3", [])
        except Exception:
            self.record = 0
            self.top3   = []

    def guardar_record(self, puntuacio, nom):
        self.top3.append((nom, puntuacio))
        self.top3.sort(key=lambda x: x[1], reverse=True)
        self.top3 = self.top3[:3]
        if puntuacio > self.record:
            self.record = puntuacio
        try:
            with open("record.json", "w") as f:
                json.dump({"puntuacio": self.record, "top3": self.top3}, f)
        except Exception:
            pass

    # ==================================================================
    # NOVA PARTIDA
    # ==================================================================
    def nova_partida(self):
        """Reinicia totes les variables per a una nova partida."""
        self.temps_restant = 120.0
        self.estat_joc     = "JUGANT"
        self.nivel_actual  = 1

        self.jugador   = Jugador(50, ALCADA // 2 - 20)
        self.llums     = SistemaLlums()
        self.puntuacio = Puntuacio(self.jugador)

        self.obstacles = [
            Obstacle(random.randint(300, META_X - 50),
                     random.randint(20, ALCADA - 50))
            for _ in range(3)
        ]
        self.powerups = []

        # Timers d'aparició d'objectes nous
        self.timer_obstacle = 0.0
        self.timer_powerup  = 0.0

    # ==================================================================
    # BUCLE PRINCIPAL
    # ==================================================================
    def executar(self):
        self.iniciar()

        # Fonts de text
        font_gran    = pygame.font.SysFont(None, 74)
        font_mitjana = pygame.font.SysFont(None, 48)
        font_petita  = pygame.font.SysFont(None, 32)
        font_xica    = pygame.font.SysFont(None, 24)

        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            # ── EVENTS ──────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    # Introducció del nom (NOM_INPUT)
                    if self.estat_joc == "NOM_INPUT":
                        if event.key == pygame.K_RETURN and self.nom_jugador.strip():
                            self.estat_joc = "MENU"
                        elif event.key == pygame.K_BACKSPACE:
                            self.nom_jugador = self.nom_jugador[:-1]
                        elif len(self.nom_jugador) < 15 and event.unicode.isprintable():
                            self.nom_jugador += event.unicode

                    # Menú principal
                    elif self.estat_joc == "MENU":
                        if event.key == pygame.K_SPACE:
                            self.nova_partida()

                    # Final de partida
                    elif self.estat_joc in ("PERDUT", "GUANYAT"):
                        if event.key == pygame.K_r:
                            self.nova_partida()
                        elif event.key == pygame.K_m:
                            self.estat_joc = "MENU"

                    # Sortida ràpida
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # ── ACTUALITZAR ──────────────────────────────────────────
            self._actualitzar_estelles()
            if self.estat_joc == "JUGANT":
                self._actualitzar_partida(dt)

            # ── DIBUIXAR ─────────────────────────────────────────────
            if self.estat_joc == "NOM_INPUT":
                self._dibuixar_input_nom(font_gran, font_mitjana, font_petita)
            elif self.estat_joc == "MENU":
                self._dibuixar_menu(font_gran, font_mitjana, font_petita, font_xica)
            elif self.estat_joc == "JUGANT":
                self._dibuixar_partida(font_petita, font_xica)
            elif self.estat_joc == "GUANYAT":
                self._dibuixar_victoria(font_gran, font_mitjana, font_petita)
            elif self.estat_joc == "PERDUT":
                self._dibuixar_game_over(font_gran, font_mitjana, font_petita, font_xica)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # ==================================================================
    # LÒGICA DE JOC
    # ==================================================================
    def _actualitzar_partida(self, dt):
        """Actualitza tots els sistemes del joc cada frame."""

        # Input i física del jugador
        tecles = pygame.key.get_pressed()
        self.jugador.gestionar_input(tecles)
        self.jugador.actualitzar(dt)

        # Sistemes principals
        self.llums.actualitzar()
        self.puntuacio.actualitzar(dt)
        self._actualitzar_temps(dt)
        self._actualitzar_nivell()

        # ── OBSTACLES ──────────────────────────────────────────────
        self.timer_obstacle += dt
        if self.timer_obstacle >= 4.0 and len(self.obstacles) < 6:
            self.timer_obstacle = 0.0
            self.obstacles.append(
                Obstacle(AMPLADA + 20, random.randint(20, ALCADA - 50))
            )

        for obs in self.obstacles[:]:
            obs.actualitzar(dt)
            if obs.rect.x < -60:
                self.obstacles.remove(obs)

        # ── POWER-UPS ───────────────────────────────────────────────
        self.timer_powerup += dt
        if self.timer_powerup >= 8.0 and len(self.powerups) < 3:
            self.timer_powerup = 0.0
            tipus = random.choice(["punts", "temps", "escut"])
            self.powerups.append(
                PowerUp(AMPLADA + 20, random.randint(20, ALCADA - 40), tipus)
            )

        for pw in self.powerups[:]:
            if not pw.actualitzar(dt):
                self.powerups.remove(pw)

        # ── COL·LISIONS ─────────────────────────────────────────────
        jugador_rect = self.jugador.get_rect()

        # Obstacles
        for obs in self.obstacles[:]:
            if jugador_rect.colliderect(obs.rect):
                self.puntuacio.punts = max(0, self.puntuacio.punts - 10)
                self.jugador.x = max(0.0, self.jugador.x - 50)
                self._reproduir_so(self.sonido_choque)
                self.obstacles.remove(obs)
                break

        # Power-ups
        for pw in self.powerups[:]:
            if jugador_rect.colliderect(pw.rect):
                self._aplicar_powerup(pw)
                self.powerups.remove(pw)

        # ── MORT PER LLUM VERMELLA ───────────────────────────────────
        if self.llums.get_estat() == "VERMELL" and self.jugador.esta_movent():
            if self.jugador.tiene_escudo:
                self.jugador.perder_escudo()
                self._reproduir_so(self.sonido_choque)
            else:
                self.estat_joc = "PERDUT"
                self.jugador.esta_viu = False
                self._reproduir_so(self.sonido_muerte)
                self.guardar_record(self.puntuacio.get_punts(), self.nom_jugador)
                return  # Aturar la resta d'actualitzacions

        # ── VICTÒRIA ─────────────────────────────────────────────────
        if self.jugador.x + self.jugador.amplada >= META_X:
            self.puntuacio.bonus_final(self.temps_restant)
            self.estat_joc = "GUANYAT"
            self._reproduir_so(self.sonido_victoria)
            self.guardar_record(self.puntuacio.get_punts(), self.nom_jugador)

    def _actualitzar_temps(self, dt):
        """Decrementa el temporitzador. Si arriba a 0, derrota."""
        self.temps_restant -= dt
        if self.temps_restant <= 0:
            self.temps_restant = 0
            self.estat_joc = "PERDUT"
            self._reproduir_so(self.sonido_muerte)
            self.guardar_record(self.puntuacio.get_punts(), self.nom_jugador)

    def _actualitzar_nivell(self):
        """Augmenta la dificultat de les llums en funció dels punts."""
        punts = self.puntuacio.get_punts()
        nou_nivell = 1 + (punts >= 300) + (punts >= 600)
        if nou_nivell != self.nivel_actual:
            self.nivel_actual = nou_nivell
            self.llums.set_nivel(self.nivel_actual)
            self._reproduir_so(self.sonido_cambio)

    def _aplicar_powerup(self, pw):
        """Aplica l'efecte d'un power-up recollit."""
        if pw.tipus == "punts":
            self.puntuacio.punts += 50
        elif pw.tipus == "temps":
            self.temps_restant = min(120.0, self.temps_restant + 5)
        elif pw.tipus == "escut":
            self.jugador.aplicar_escudo()
        self._reproduir_so(self.sonido_powerup)

    # ==================================================================
    # DIBUIX — PANTALLES
    # ==================================================================
    def _dibuixar_input_nom(self, font_gran, font_mitjana, font_petita):
        """Pantalla inicial d'introducció del nom del jugador."""
        self.pantalla.fill((5, 5, 20))
        self._dibuixar_estelles()

        titol = font_gran.render("SPACE RUN 🚀", True, (100, 200, 255))
        self.pantalla.blit(titol, (AMPLADA // 2 - titol.get_width() // 2, 120))

        msg = font_mitjana.render("Introdueix el teu nom:", True, (200, 200, 255))
        self.pantalla.blit(msg, (AMPLADA // 2 - msg.get_width() // 2, 250))

        # Caixa de text
        box_rect = pygame.Rect(200, 310, 400, 50)
        pygame.draw.rect(self.pantalla, (30, 30, 60), box_rect)
        pygame.draw.rect(self.pantalla, (100, 180, 255), box_rect, 2)

        nom_text = font_mitjana.render(self.nom_jugador + "|", True, (255, 255, 255))
        self.pantalla.blit(nom_text, (box_rect.x + 10, box_rect.y + 8))

        enter_msg = font_petita.render("Prem ENTER per continuar", True, (150, 150, 200))
        self.pantalla.blit(enter_msg, (AMPLADA // 2 - enter_msg.get_width() // 2, 390))

    def _dibuixar_menu(self, font_gran, font_mitjana, font_petita, font_xica):
        """Pantalla de menú principal amb instruccions i top 3."""
        self.pantalla.fill((5, 5, 20))
        self._dibuixar_estelles()

        titol = font_gran.render("SPACE RUN", True, (100, 200, 255))
        self.pantalla.blit(titol, (AMPLADA // 2 - titol.get_width() // 2, 60))

        sub = font_mitjana.render("Reacció Ràpida Espacial", True, (150, 200, 255))
        self.pantalla.blit(sub, (AMPLADA // 2 - sub.get_width() // 2, 140))

        instruccions = [
            ("Creua el passadís fins a la meta",     (200, 200, 200)),
            ("🟢 Llum VERDA → pots avançar",         (100, 255, 100)),
            ("🔴 Llum VERMELLA → atura't! (mor!)",   (255, 100, 100)),
            ("⬆⬇⬅➡ / WASD per moure la nau",        (180, 180, 255)),
            ("⏱  Tens 120 segons",                    (200, 200, 200)),
        ]
        for i, (text, color) in enumerate(instruccions):
            surf = font_petita.render(text, True, color)
            self.pantalla.blit(surf, (AMPLADA // 2 - surf.get_width() // 2, 210 + i * 38))

        # Top 3
        top_surf = font_petita.render("🏆 TOP 3 🏆", True, (255, 215, 0))
        self.pantalla.blit(top_surf, (AMPLADA // 2 - top_surf.get_width() // 2, 420))
        for i, (nom, punts) in enumerate(self.top3):
            t = font_xica.render(f"{i+1}. {nom}: {punts}", True, (255, 255, 200))
            self.pantalla.blit(t, (AMPLADA // 2 - t.get_width() // 2, 455 + i * 22))

        start = font_mitjana.render("Pressiona SPACE per jugar", True, (100, 255, 100))
        self.pantalla.blit(start, (AMPLADA // 2 - start.get_width() // 2, 555))

    def _dibuixar_partida(self, font_petita, font_xica):
        """Dibuixa el joc en curs: fons, meta, obstacles, jugador i HUD."""
        # Fons de color depenent de la llum
        self.pantalla.fill(self.llums.get_color_fons())
        self._dibuixar_estelles()

        # Zona de meta
        pygame.draw.rect(self.pantalla, (255, 215, 0), (META_X, 0, AMPLADA - META_X, ALCADA))
        meta_text = font_xica.render("META", True, (0, 0, 0))
        self.pantalla.blit(meta_text, (META_X + 5, ALCADA // 2 - 10))

        # Obstacles i power-ups
        for obs in self.obstacles:
            obs.dibuixar(self.pantalla)
        for pw in self.powerups:
            pw.dibuixar(self.pantalla)

        # Barra de progrés
        self._dibuixar_barra_progres()

        # Jugador
        self.jugador.dibuixar(self.pantalla)

        # HUD
        color_llum = (100, 255, 100) if self.llums.get_estat() == "VERD" else (255, 80, 80)
        llum_txt = "🟢 VERD" if self.llums.get_estat() == "VERD" else "🔴 VERMELL"
        self.pantalla.blit(font_petita.render(llum_txt, True, color_llum), (AMPLADA - 180, 10))

        color_temps = (255, 80, 80) if self.temps_restant < 20 else (0, 0, 0)
        self.pantalla.blit(
            font_petita.render(f"⏱ {int(self.temps_restant)}s", True, color_temps), (10, 10))
        self.pantalla.blit(
            font_petita.render(f"Punts: {self.puntuacio.get_punts()}", True, (0, 0, 0)), (10, 48))
        self.pantalla.blit(
            font_petita.render(f"Nivell: {self.nivel_actual}", True, (0, 0, 0)), (10, 86))

        if self.jugador.tiene_escudo:
            self.pantalla.blit(
                font_xica.render("🛡 Escut actiu", True, (0, 255, 100)), (10, 124))

    def _dibuixar_barra_progres(self):
        """Barra horitzontal de progrés cap a la meta."""
        bx, by, bw, bh = 20, ALCADA - 28, AMPLADA - 40, 16
        pygame.draw.rect(self.pantalla, (80, 80, 80), (bx, by, bw, bh))
        progress = min(1.0, self.jugador.x / META_X) * bw
        pygame.draw.rect(self.pantalla, (100, 200, 255), (bx, by, int(progress), bh))
        pygame.draw.rect(self.pantalla, (180, 180, 180), (bx, by, bw, bh), 2)

    def _dibuixar_victoria(self, font_gran, font_mitjana, font_petita):
        """Pantalla de victòria."""
        self.pantalla.fill((20, 50, 20))
        self._dibuixar_estelles()

        titol = font_gran.render("¡VICTÒRIA! 🎉", True, (100, 255, 100))
        self.pantalla.blit(titol, (AMPLADA // 2 - titol.get_width() // 2, 80))

        punts = self.puntuacio.get_punts()
        self.pantalla.blit(
            font_mitjana.render(f"Punts finals: {punts}", True, (150, 255, 150)),
            (AMPLADA // 2 - 180, 200))

        record_txt = "🏆 NOU RÈCORD!" if punts >= self.record else f"Rècord: {self.record}"
        self.pantalla.blit(
            font_petita.render(record_txt, True, (255, 215, 0)),
            (AMPLADA // 2 - 140, 280))

        for i, txt in enumerate([
            "R → Jugar de nou",
            "M → Menú principal",
        ]):
            surf = font_petita.render(txt, True, (200, 255, 200))
            self.pantalla.blit(surf, (AMPLADA // 2 - surf.get_width() // 2, 400 + i * 40))

    def _dibuixar_game_over(self, font_gran, font_mitjana, font_petita, font_xica):
        """Pantalla de derrota."""
        self.pantalla.fill((50, 15, 15))
        self._dibuixar_estelles()

        titol = font_gran.render("GAME OVER 💀", True, (255, 80, 80))
        self.pantalla.blit(titol, (AMPLADA // 2 - titol.get_width() // 2, 80))

        punts = self.puntuacio.get_punts()
        self.pantalla.blit(
            font_mitjana.render(f"Punts: {punts}", True, (255, 140, 140)),
            (AMPLADA // 2 - 120, 200))

        if self.temps_restant <= 0:
            motiu = "S'ha acabat el temps!"
        else:
            motiu = "T'has mogut en llum vermella!"
        self.pantalla.blit(
            font_petita.render(motiu, True, (255, 140, 140)),
            (AMPLADA // 2 - 200, 290))

        self.pantalla.blit(
            font_xica.render(f"Rècord: {self.record}", True, (200, 200, 200)),
            (AMPLADA // 2 - 80, 345))

        for i, txt in enumerate([
            "R → Jugar de nou",
            "M → Menú principal",
        ]):
            surf = font_petita.render(txt, True, (200, 200, 200))
            self.pantalla.blit(surf, (AMPLADA // 2 - surf.get_width() // 2, 410 + i * 40))