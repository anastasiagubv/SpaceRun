# 🤖 Registre d'ús de la IA

## Prompt 1 (Fase 1)
**Prompt:** "Com puc detectar si un jugador es mou en Pygame?"
**Resposta IA:** Comprovar `player.vel_x != 0` o comparar posicions entre frames.
**Decisió:** He optat per `vel_x != 0` perquè és més eficient.

## Prompt 2 (Fase 1)
**Prompt:** "Com faig un temporitzador que no depengui dels FPS?"
**Resposta:** Usar `pygame.time.get_ticks()` per mesurar temps real.
**Decisió:** Implementat a `SistemaLlums` i `GestorJoc`.

## Prompt 3 (Fase 3)
**Prompt:** "Com puc fer que el jugador no surti de la pantalla?"
**Resposta:** `rect.clamp_ip(pygame.Rect(0,0, ample, alt))`
**Decisió:** Usat, però finalment ho he fet manual amb condicions `if x < 0: x = 0` per més control.

## Prompt 4 (Fase 4)
**Prompt:** "Com puc simular un efecte de partícules senzill per a l'estela?"
**Resposta:** Guardar posicions anteriors en una llista i dibuixar cercles amb opacitat decreixent.
**Decisió:** Implementat a `Jugador.dibuixar()`.

## Prompt 5 (Fase 5)
**Prompt:** "Com puc fer que la dificultat augmenti cada cert temps?"
**Resposta:** Reduir l'interval de canvi de llum progressivament.
**Decisió:** Afegit mètode `actualitzar_dificultat` a `GestorJoc`.