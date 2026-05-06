# 🚀 Fase 5: Millores i Reflexió Final

> **Projecte:** Space Run  
> **Data:** 2026-05-06  

---

## ✨ 1. Millores implementades

A partir del prototip inicial de la Fase 3, s'han implementat les següents millores per convertir-lo en un joc complet:

* **Condició de Victòria:** S'ha afegit una zona segura (meta groga) a la part superior. Si el jugador hi arriba, guanya la partida.
* **Condició de Derrota (Game Over):** El joc ara atura l'acció i mostra una pantalla negra si el jugador es mou quan la llum és vermella.
* **Sistema de Reinici:** S'ha implementat la possibilitat de prémer la tecla `R` per reiniciar la posició del jugador i el temporitzador de les llums sense haver de tancar el programa.
* **Interfície d'Usuari (UI):** S'han afegit textos a la pantalla (usant `pygame.font`) per comunicar l'estat del joc (Victòria o Game Over) de forma clara.

---

## 🔮 2. Possibles millores futures

Si tingués més temps per expandir el projecte, m'agradaria afegir:

1. **Efectes de so:** Un so d'alarma per a la llum vermella i un so d'èxit en arribar a la meta.
2. **Nivells de dificultat:** Fer que la franja de temps de llum verda sigui cada vegada més curta a mesura que se superen nivells.
3. **Obstacles mòbils:** Afegir asteroides o làsers que s'hagin d'esquivar pel passadís mentre es respecten les llums.

---

## 🧠 3. Reflexió final sobre el Vibe Coding

L'experiència de desenvolupar aquest microvideojoc utilitzant assistència d'Intel·ligència Artificial (Vibe Coding) ha estat molt positiva, però també ha presentat reptes tècnics interessants:

* **El que ha anat millor:** La IA ha estat clau per muntar ràpidament l'estructura del bucle principal de Pygame i per solucionar la lògica matemàtica (com evitar que el jugador surti de la pantalla amb `clamp_ip`). Ha accelerat molt el procés d'escriptura de codi rutinari.
* **Els reptes superats:** He après que l'entorn de treball és fonamental. He hagut d'enfrontar-me a problemes de configuració amb els entorns virtuals (`venv`), permisos de PowerShell a Windows i gestió de repositoris Git (`git init`). L'assistent m'ha guiat, però he hagut d'interpretar els errors de la terminal i aplicar les solucions al meu equip.
* **Conclusió:** El *Vibe Coding* no consisteix només a fer "copiar i enganxar", sinó a saber quines preguntes fer, entendre on posar el codi generat i, sobretot, saber com depurar els errors de configuració de l'entorn.