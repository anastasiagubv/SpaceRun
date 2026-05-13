# 🚀 Space Run

**Microvideojoc de reacció ràpida** desenvolupat amb Python i Pygame per a l'assignatura d'Entorns de Desenvolupament.

## 📝 Descripció

Controla una nau espacial que ha de creuar un passadís ple de trampes de seguretat. Només pots avançar quan la llum estigui **VERDA**. Si et mous durant la llum **VERMELLA**, explotes!

## 🎮 Com jugar

- **MOVIMENT**: Tecles `D` o `→` (dreta) i `A` o `←` (esquerra)
- **OBJECTIU**: Arribar a la franja groga (càpsula d'escapament) abans que s'acabi el temps (120 segons)
- **REGLES**:
  - 🟢 Llum VERDA → pots moure't lliurement
  - 🔴 Llum VERMELLA → has d'estar completament aturat
  - ⏱️ Com més ràpid arribis, més punts (bonus per temps restant)
  - 🏆 La dificultat augmenta cada 10 segons (els canvis de llum són més ràpids)

## 📥 Instal·lació

```bash
# Clona el repositori
git clone https://github.com/el-teu-usuari/space-run.git
cd space-run

# Instal·la Pygame
pip install pygame

# Executa el joc
python main.py