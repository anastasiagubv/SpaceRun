# 🚀 Fase 1: Exploració de la Idea i Delimitació de l’Abast
> **Projecte:** Space Run
> **Entorn:** Roblox Studio / Luau

---

## 🌌 1. Títol provisional del joc
**"SPACE RUN"**

## 🕹️ 2. Tipus de microvideojoc escollit
Joc de supervivència i reacció basat en **estats lògics** (Llum Roja / Llum Verda) en un entorn 3D.

## 🎯 3. Objectiu del joc
El jugador ha de creuar un passadís espacial i arribar a la meta (càpsula d'escapament) abans que s'acabi el temps, aturant-se completament quan el sistema de seguretat es posa en vermell.

## 👤 4. Rol del jugador
* **Control:** L'usuari controla un avatar en tercera persona.
* **Accions:** Moure's (WASD) i saltar (Espai).
* **Responsabilitat:** Gestionar la frenada per no moure's gens durant la fase de perill.

## 📜 5. Regles bàsiques
1.  **Llum Verda:** El jugador pot avançar cap a la meta.
2.  **Llum Roja:** El jugador s'ha d'aturar. Qualsevol moviment detectat provoca la mort instantània.
3.  **Temps:** Hi ha un límit de 120 segons per guanyar.

## 🏆 6. Condicions de victòria i derrota
* **Victòria:** Arribar a la part que defineix la meta.
* **Derrota:** Moure's en Llum Roja o que el comptador arribi a zero.

## 🔄 7. Bucle principal del joc (Game Loop)
1.  **Inici:** Apareixes a la sortida.
2.  **Observació:** Mirar el color de les llums del passadís.
3.  **Acció:** Córrer (Verd) o Aturar-se (Vermell).
4.  **Repetició:** Avançar per trams fins a la meta.

## 📈 8. Repte principal i dificultat
El repte és la **reacció**. La dificultat és **mitjana**, ja que els canvis de llum seran aleatoris per evitar que el jugador aprengui el ritme de memòria.

## 🚫 9. Limitacions explícites (Què NO inclourà)
* No hi haurà multijugador.
* No hi haurà enemics mòbils ni armes.
* No hi haurà botiga ni inventari.

## ⚠️ 10. Riscos tècnics
1.  **Detecció de moviment:** Ajustar bé la sensibilitat perquè el personatge mori si es mou, però no per petits errors de la càmera.
2.  **Sincronització:** Que la llum visual i la lògica de "mort" canviïn exactament alhora.
3.  **Inèrcia:** Evitar que el jugador mori per la pròpia inèrcia del salt en entrar en fase vermella.

## 🤖 11. Exploració amb IA (Mínim 2 prompts)
* **Prompt 1:** "Com puc detectar si un jugador es mou a Roblox usant Humanoid.MoveDirection?" -> *Resposta:* La IA suggereix comprovar si la magnitud de MoveDirection és major que 0.
* **Prompt 2:** "Fes un script simple per canviar el color d'una peça de verd a vermell cada pocs segons." -> *Resposta:* La IA proposa un bucle `while true` amb `wait(math.random(2,5))`.

## ✅ 12. Proposta final escollida
Desenvolupar **Space Run**: un joc de reacció ràpida en una nau espacial amb estètica neó.

## 💡 13. Justificació de viabilitat
És totalment viable perquè només requereix un script principal de control i un disseny de mapa senzill, encaixant perfectament en les 10 hores de feina.

## 📅 14. Mini pla de treball (10h)
* **Hores 1-2:** Disseny del mapa (passadís i meta).
* **Hores 3-6:** Programació del sistema Llum Roja/Verda i detecció de moviment.
* **Hores 7-8:** Interfície (UI) de temps i estat.
* **Hores 9-10:** Proves i correcció d'errors.

## 🛠️ 15. Eines previstes i justificació
* **Roblox Studio:** Motor per crear el joc.
* **Luau:** Llenguatge necessari per a la programació.
* **ChatGPT:** Com a suport per resoldre dubtes de codi.