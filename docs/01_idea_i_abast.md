# 🚀 Fase 1: Exploració de la Idea i Delimitació de l'Abast
> **Projecte:** Space Run
> **Entorn:** Python + Pygame

---

## 🌌 1. Títol provisional del joc
**"SPACE RUN"**

## 🕹️ 2. Tipus de microvideojoc escollit
Joc de supervivència i reacció basat en **estats lògics** (Llum Roja / Llum Verda) en un entorn 2D visual.

## 🎯 3. Objectiu del joc
El jugador ha de creuar un passadís espacial i arribar a la meta (càpsula d'escapament) abans que s'acabi el temps, aturant-se completament quan el sistema de seguretat es posa en vermell.

## 👤 4. Rol del jugador
* **Control:** L'usuari controla un avatar en vista lateral 2D.
* **Accions:** Moure's (tecles esquerra/dreta o WASD).
* **Responsabilitat:** Gestionar la frenada per no moure's gens durant la fase de perill.

## 📜 5. Regles bàsiques
1. **Llum Verda:** El jugador pot avançar cap a la meta.
2. **Llum Roja:** El jugador s'ha d'aturar. Qualsevol moviment detectat provoca la mort instantània.
3. **Temps:** Hi ha un límit de 120 segons per guanyar.

## 🏆 6. Condicions de victòria i derrota
* **Victòria:** Arribar a la zona de meta (càpsula d'escapament).
* **Derrota:** Moure's en Llum Roja o que el comptador arribi a zero.

## 🔄 7. Bucle principal del joc (Game Loop)
1. **Inici:** L'avatar apareix a l'extrem esquerre del passadís.
2. **Observació:** El jugador mira el color de fons / indicador de llum.
3. **Acció:** Moure's (Verd) o aturar-se (Vermell).
4. **Repetició:** Avançar tram a tram fins a arribar a la meta.

## 📈 8. Repte principal i dificultat
El repte és la **reacció**. La dificultat és **mitjana**, ja que els canvis de llum seran aleatoris (entre 2 i 5 segons) per evitar que el jugador aprengui el ritme de memòria.

## 🚫 9. Limitacions explícites (Què NO inclourà)
* No hi haurà multijugador.
* No hi haurà enemics mòbils ni armes.
* No hi haurà botiga ni inventari.
* No hi haurà animacions complexes ni sprites externs.

## ⚠️ 10. Riscos tècnics
1. **Detecció de moviment:** Distingir entre el jugador movent-se activament i petites variacions de posició degudes a la inèrcia o al codi.
2. **Sincronització visual:** Que el canvi de color de pantalla i la lògica de mort es produeixin exactament al mateix frame.
3. **Gestió del temps:** Que el temporitzador de 120 s funcioni de manera precisa i no depengui dels FPS del joc.

## 🤖 11. Exploració amb IA (Mínim 2 prompts)
* **Prompt 1:** "Com puc detectar si un jugador es mou en Pygame?" → *Resposta:* La IA suggereix comprovar si `player.vel_x != 0` o si la posició ha canviat respecte al frame anterior.
* **Prompt 2:** "Com faig un temporitzador que no depengui dels FPS a Pygame?" → *Resposta:* La IA proposa usar `pygame.time.get_ticks()` per mesurar mil·lisegons reals i calcular el temps transcorregut independent dels frames.

## ✅ 12. Proposta final escollida
Desenvolupar **Space Run**: un joc de reacció ràpida en un passadís espacial 2D amb estètica neó, implementat amb Python i Pygame.

## 💡 13. Justificació de viabilitat
És totalment viable perquè Pygame ofereix les eines necessàries (detecció de tecles, dibuix de formes, gestió del temps) sense necessitat de llibreries complexes. L'estructura del joc és simple i encaixa perfectament en les 10 hores de feina disponibles.

## 📅 14. Mini pla de treball (10h)
* **Hores 1-2:** Disseny del mapa (passadís, avatar i meta amb `pygame.draw`).
* **Hores 3-6:** Programació del sistema Llum Roja/Verda, detecció de moviment i lògica de mort.
* **Hores 7-8:** Interfície (UI): temporitzador, indicador d'estat i pantalles de victòria/derrota.
* **Hores 9-10:** Proves, correcció d'errors i millores.

## 🛠️ 15. Eines previstes i justificació
* **Python 3:** Llenguatge principal. Sintaxi clara i gran comunitat.
* **Pygame:** Llibreria per a jocs 2D. Gestiona finestra, events, dibuix i temps.
* **VS Code:** IDE lleuger amb extensió de Python i debugger integrat.
* **GitHub:** Control de versions i lliurament del projecte.
* **Claude / ChatGPT:** Suport per resoldre dubtes de codi i generar idees.