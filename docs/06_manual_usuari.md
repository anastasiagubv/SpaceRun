# Manual d'usuari

## Nom del joc

Space Run

## Objectiu del joc

El jugador controla una nau espacial que ha d'arribar a la zona d'escapament abans que s'acabi el temps.

Durant la partida, el sistema de seguretat alterna entre llum verda i llum vermella.

* Amb llum verda es pot moure.
* Amb llum vermella no es pot moure.

Si el jugador es mou durant la llum vermella, perd la partida.

## Com iniciar el joc

```bash
python main.py
```

## Controls

| Acció          | Tecla |
| -------------- | ----- |
| Moure dreta    | D o → |
| Moure esquerra | A o ← |
| Moure amunt    | W o ↑ |
| Moure avall    | S o ↓ |

## Regles del joc

1. Arribar a la meta abans que s'acabi el temps.
2. Evitar obstacles.
3. Recollir power-ups per obtenir avantatges.
4. No moure's durant la llum vermella.

## Condicions de victòria

* Arribar a la zona de meta.

## Condicions de derrota

* Moure's durant la llum vermella.
* Quedar-se sense temps.

## Exemple de partida

1. El jugador inicia la partida.
2. Espera la llum verda.
3. Avança cap a la meta evitant obstacles.
4. Recull power-ups.
5. Arriba a la meta i obté la victòria.

## Problemes coneguts

* Alguns obstacles poden aparèixer molt a prop del jugador.
* La dificultat augmenta ràpidament als nivells superiors.
