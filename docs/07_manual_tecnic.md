# Manual tècnic

## Arquitectura general

El projecte Space Run està desenvolupat en Python utilitzant la llibreria Pygame.

La lògica es divideix en diferents classes per separar responsabilitats.

## Estructura de carpetes

```plaintext
src/
docs/
sounds/
tests/
evidencies/
```

## Components principals

| Component    | Fitxer          | Responsabilitat                 |
| ------------ | --------------- | ------------------------------- |
| GestorJoc    | gestorJoc.py    | Control del joc                 |
| Jugador      | jugador.py      | Moviment i estat del jugador    |
| SistemaLlums | sistemaLlums.py | Gestió de llum verda i vermella |
| Puntuacio    | puntuacio.py    | Sistema de puntuació            |
| Obstacle     | obstacle.py     | Obstacles del nivell            |
| PowerUp      | powerUp.py      | Objectes especials              |

## Flux principal

1. S'inicialitza Pygame.
2. Es crea el GestorJoc.
3. Comença el bucle principal.
4. Es processen entrades del teclat.
5. S'actualitza l'estat del joc.
6. Es dibuixen els elements.
7. Es comproven victòria o derrota.

## Decisions tècniques

| Decisió           | Justificació               |
| ----------------- | -------------------------- |
| Python + Pygame   | Desenvolupament ràpid      |
| Classes separades | Millor manteniment         |
| Sistema de llums  | Mecànica principal del joc |
| Power-ups         | Augmentar la jugabilitat   |

## Millores futures

* Nous nivells.
* Nous enemics.
* Sistema de guardat.
* Mode multijugador.
* Millora gràfica.
