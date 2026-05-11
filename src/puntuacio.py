class Puntuacio:
    """Gestiona el sistema de puntuació del joc"""
    
    def __init__(self, jugador):
        self.jugador = jugador
        self.punts = 0
        self.distancia_anterior = 0
    
    def actualitzar(self, dt):
        """Actualiza la puntuación cada frame"""
        # Punts per distancia (1 punt per cada pixel avançat)
        distancia_actual = int(self.jugador.x)
        if distancia_actual > self.distancia_anterior:
            punts_distancia = distancia_actual - int(self.distancia_anterior)
            self.punts += punts_distancia
            self.distancia_anterior = distancia_actual
        
        # Bonus de temps (0.1 punts per segon restant)
        # Això es calcularà al final de la partida
    
    def get_punts(self):
        """Retorna els punts actuals"""
        return self.punts
    
    def bonus_final(self, temps_restant):
        """Aplica bonus final segons el temps"""
        bonus = int(temps_restant * 10)  # 10 punts per segon
        self.punts += bonus
        return bonus