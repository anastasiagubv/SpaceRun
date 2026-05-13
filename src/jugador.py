import pygame

class Jugador:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.esta_viu = True
        self.amplada = 40
        self.alcada = 40
        self.velocitat_base = 300  # píxels/segon
        self.parpelleja_timer = 0
        self.visible = True
        self.estela_posiciones = []
        # Nuevo: escudo activo
        self.tiene_escudo = False

    def gestionar_input(self, tecles):
        # Moviment horitzontal
        self.vel_x = 0.0
        if tecles[pygame.K_RIGHT] or tecles[pygame.K_d]:
            self.vel_x = self.velocitat_base
        elif tecles[pygame.K_LEFT] or tecles[pygame.K_a]:
            self.vel_x = -self.velocitat_base

        # Moviment vertical
        self.vel_y = 0.0
        if tecles[pygame.K_DOWN] or tecles[pygame.K_s]:
            self.vel_y = self.velocitat_base
        elif tecles[pygame.K_UP] or tecles[pygame.K_w]:
            self.vel_y = -self.velocitat_base

    def actualitzar(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        # Límits horitzontals (0 fins a amplada - amplada_jugador)
        if self.x < 0:
            self.x = 0
        if self.x > 800 - self.amplada:
            self.x = 800 - self.amplada

        # Límits verticals (0 fins a alcada - alcada_jugador)
        if self.y < 0:
            self.y = 0
        if self.y > 600 - self.alcada:
            self.y = 600 - self.alcada

        # Estela (solo si se mueve horizontal o verticalmente)
        if self.esta_viu and (self.vel_x != 0 or self.vel_y != 0):
            self.estela_posiciones.append((self.x + self.amplada//2, self.y + self.alcada//2))
            if len(self.estela_posiciones) > 15:
                self.estela_posiciones.pop(0)
        else:
            self.estela_posiciones.clear()

        if not self.esta_viu:
            self.parpelleja_timer += dt
            if self.parpelleja_timer > 0.15:
                self.visible = not self.visible
                self.parpelleja_timer = 0

    def esta_movent(self):
        return self.vel_x != 0 or self.vel_y != 0

    def dibuixar(self, pantalla):
        if not self.esta_viu and not self.visible:
            return

        # Dibuixar estela (partícules)
        for i, pos in enumerate(self.estela_posiciones):
            alpha = max(0, 255 - i * 20)
            color = (200, 100, 50)
            pygame.draw.circle(pantalla, color, (int(pos[0]), int(pos[1])), max(1, 5 - i//3))

        # Cos principal (triangle)
        center_x = self.x + self.amplada // 2
        center_y = self.y + self.alcada // 2

        if self.esta_viu:
            # Color según tenga escudo o no
            if self.tiene_escudo:
                color_nau = (0, 255, 150)   # Verde brillante
                color_borde = (150, 255, 150)
            else:
                color_nau = (50, 150, 255)
                color_borde = (100, 200, 255)

            punta = (center_x + 15, center_y)
            base1 = (center_x - 10, center_y - 15)
            base2 = (center_x - 10, center_y + 15)
            pygame.draw.polygon(pantalla, color_nau, [punta, base1, base2])
            pygame.draw.polygon(pantalla, color_borde, [punta, base1, base2], 2)
            # Motor (llama)
            if self.vel_x > 0:
                llama = [(center_x - 15, center_y), (center_x - 5, center_y - 8), (center_x - 5, center_y + 8)]
                pygame.draw.polygon(pantalla, (255, 100, 0), llama)
        else:
            # Nau destruïda
            pygame.draw.polygon(pantalla, (100, 100, 100), [(center_x + 15, center_y), (center_x - 10, center_y - 15), (center_x - 10, center_y + 15)])
            pygame.draw.line(pantalla, (255, 0, 0), (center_x - 5, center_y - 5), (center_x + 5, center_y + 5), 3)
            pygame.draw.line(pantalla, (255, 0, 0), (center_x + 5, center_y - 5), (center_x - 5, center_y + 5), 3)
            
        @property
        def rect(self):
            return pygame.Rect(self.x, self.y, self.amplada, self.alcada)