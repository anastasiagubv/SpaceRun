# 🐛 Fase 4: Proves i depuració

> **Projecte:** Space Run  
> **Data:** 2026-05-06  

---

## 🧪 1. Casos de prova (Test Cases)

S'han definit i executat les següents proves per comprovar que la mecànica principal funciona correctament:

| ID | Descripció de la prova | Acció de l'usuari | Resultat esperat | Resultat obtingut | Estat |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **01** | Moviment del jugador | Prémer tecles WASD o Fletxes | El quadrat blau es mou en la direcció indicada i no surt de la pantalla. | El jugador es mou correctament i es manté dins dels límits. | ✅ Passa |
| **02** | Canvi de llums (Verd/Vermell) | Observar la pantalla | El fons canvia de verd a vermell de forma aleatòria cada pocs segons. | El temporitzador intern funciona i canvia els colors correctament. | ✅ Passa |
| **03** | Detecció de mort (Llum vermella) | Moure's mentre el fons és vermell | El joc detecta la infracció i activa l'estat de "Game Over". | *S'ha implementat primer per consola i després visualment.* | ✅ Passa |

---

## 🐞 2. Bugs detectats i solucionats

Durant el desenvolupament i les proves, s'han trobat els següents problemes:

* **Bug 1:** El jugador podia sortir-se de la pantalla per les vores.
    * *Causa:* No hi havia cap límit matemàtic per a les coordenades `x` i `y` del jugador.
    * *Solució:* S'ha utilitzat la funció `self.rect.clamp_ip(pygame.Rect(0, 0, AMPLADA, ALÇADA))` de Pygame per mantenir el rectangle sempre dins de la finestra.
* **Bug 2:** El joc detectava "mort" fins i tot si deixaves anar la tecla just en posar-se vermell, per inèrcia de la variable de moviment.
    * *Causa:* La variable `self.movent` no es reiniciava a `False` al principi de cada frame.
    * *Solució:* S'ha afegit `self.movent = False` a la primera línia del mètode `actualitzar(self, tecles)` del jugador perquè només sigui `True` si la tecla està activament premuda en aquell frame exacte.

---

## 🛠️ 3. Eines de depuració utilitzades

Per identificar i solucionar aquests errors s'han utilitzat les següents tècniques:
1.  **Impressores per consola (`print()`):** Utilitzades a la Fase 3 per comprovar que la detecció de la llum vermella funcionava (`print("¡Alerta! Te has movido en luz roja.")`) abans de programar la pantalla de Game Over.
2.  **Subratllat d'errors del VS Code (Pylance):** Per detectar errors de sintaxi en temps real (com parèntesis no tancats o imports no resolts).

| **04** | Temporitzador | Esperar 10 segons | El temps restant disminueix de 120 a 110 | Disminueix correctament | ✅ Passa |
| **05** | Guardar rècord | Guanyar una partida amb 800 punts | El fitxer `record.json` s'actualitza a 800 | S'actualitza | ✅ Passa |