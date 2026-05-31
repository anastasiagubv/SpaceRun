import pygame


class Jugador:
    """Representa l'avatar del jugador (nau espacial)."""

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.esta_viu = True
        self.amplada = 40
        self.alcada = 40
        self.velocitat_base = 300       # píxels per segon
        self.parpelleja_timer = 0.0
        self.visible = True
        self.estela_posicions = []
        self.tiene_escudo = False       # estat de l'escut

    # ------------------------------------------------------------------
    # INPUT
    # ------------------------------------------------------------------
    def gestionar_input(self, tecles):
        """Llegeix les tecles premudes i assigna velocitats."""
        # Moviment horitzontal
        self.vel_x = 0.0
        if tecles[pygame.K_RIGHT] or tecles[pygame.K_d]:
            self.vel_x = self.velocitat_base
        elif tecles[pygame.K_LEFT] or tecles[pygame.K_a]:
            self.vel_x = -self.velocitat_base

        # Moviment vertical (per esquivar obstacles)
        self.vel_y = 0.0
        if tecles[pygame.K_DOWN] or tecles[pygame.K_s]:
            self.vel_y = self.velocitat_base
        elif tecles[pygame.K_UP] or tecles[pygame.K_w]:
            self.vel_y = -self.velocitat_base

    # ------------------------------------------------------------------
    # ACTUALITZAR
    # ------------------------------------------------------------------
    def actualitzar(self, dt):
        """Aplica física, límits de pantalla i efecte d'estela."""
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        # Límits de pantalla
        self.x = max(0.0, min(self.x, 800.0 - self.amplada))
        self.y = max(0.0, min(self.y, 600.0 - self.alcada))

        # Estela de partícules (només si es mou)
        if self.esta_viu and (self.vel_x != 0 or self.vel_y != 0):
            self.estela_posicions.append(
                (self.x + self.amplada // 2, self.y + self.alcada // 2)
            )
            if len(self.estela_posicions) > 15:
                self.estela_posicions.pop(0)
        else:
            self.estela_posicions.clear()

        # Parpelleig quan la nau és destruïda
        if not self.esta_viu:
            self.parpelleja_timer += dt
            if self.parpelleja_timer > 0.15:
                self.visible = not self.visible
                self.parpelleja_timer = 0.0

    # ------------------------------------------------------------------
    # COL·LISIÓ
    # ------------------------------------------------------------------
    def get_rect(self):
        """Retorna el rectangle de col·lisió del jugador."""
        return pygame.Rect(int(self.x), int(self.y), self.amplada, self.alcada)

    # ------------------------------------------------------------------
    # ESTAT
    # ------------------------------------------------------------------
    def esta_movent(self):
        """Retorna True si el jugador s'està movent en qualsevol direcció."""
        return self.vel_x != 0 or self.vel_y != 0

    def aplicar_escudo(self):
        """Activa l'escut protector."""
        self.tiene_escudo = True

    def perder_escudo(self):
        """Desactiva l'escut protector."""
        self.tiene_escudo = False

    # ------------------------------------------------------------------
    # DIBUIXAR
    # ------------------------------------------------------------------
    def dibuixar(self, pantalla):
        """Dibuixa la nau, l'estela i l'efecte d'escut."""
        if not self.esta_viu and not self.visible:
            return

        # Estela de partícules
        for i, pos in enumerate(self.estela_posicions):
            radi = max(1, 5 - i // 3)
            pygame.draw.circle(pantalla, (200, 100, 50),
                               (int(pos[0]), int(pos[1])), radi)

        center_x = int(self.x + self.amplada // 2)
        center_y = int(self.y + self.alcada // 2)

        if self.esta_viu:
            # Color segons si té escut
            color_nau   = (0, 255, 150)   if self.tiene_escudo else (50, 150, 255)
            color_borde = (150, 255, 150) if self.tiene_escudo else (100, 200, 255)

            # Triangle principal (forma de nau)
            punta = (center_x + 15, center_y)
            base1 = (center_x - 10, center_y - 15)
            base2 = (center_x - 10, center_y + 15)
            pygame.draw.polygon(pantalla, color_nau,   [punta, base1, base2])
            pygame.draw.polygon(pantalla, color_borde, [punta, base1, base2], 2)

            # Flama del motor (visible quan avança)
            if self.vel_x > 0:
                llama = [
                    (center_x - 15, center_y),
                    (center_x - 5,  center_y - 8),
                    (center_x - 5,  center_y + 8),
                ]
                pygame.draw.polygon(pantalla, (255, 140, 0), llama)

            # Halo d'escut
            if self.tiene_escudo:
                pygame.draw.circle(pantalla, (0, 255, 150),
                                   (center_x, center_y), 25, 2)
        else:
            # Nau destruïda
            pygame.draw.polygon(
                pantalla, (100, 100, 100),
                [(center_x + 15, center_y),
                 (center_x - 10, center_y - 15),
                 (center_x - 10, center_y + 15)]
            )
            pygame.draw.line(pantalla, (255, 0, 0),
                             (center_x - 5, center_y - 5), (center_x + 5, center_y + 5), 3)
            pygame.draw.line(pantalla, (255, 0, 0),
                             (center_x + 5, center_y - 5), (center_x - 5, center_y + 5), 3)