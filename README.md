# IA - Laborator 06 (CoppeliaSim + Python)

Acest proiect contine rezolvarile pentru cerintele de laborator 3.1-3.6 si temele A, B, C, D.

## 1. Continut

### Cerinte laborator
- `cerinta_3_1_conectare.py` - conectare la CoppeliaSim si inspectie scena
- `cerinta_3_2_patrat.py` - miscare in patrat (open-loop)
- `cerinta_3_3_senzori.py` - dashboard senzori ultrasonici
- `cerinta_3_4_stop_obstacol.py` - oprire reactiva la obstacol frontal
- `cerinta_3_5_braitenberg.py` - vehicul Braitenberg "Frica" (evitare)
- `cerinta_3_6_wall_following.py` - urmarire perete dreapta (controller P)

### Teme
- `tema/tema_a_recuperare.py` - Tema A: evitare cu recuperare (masina de stari)
- `tema/tema_b_logging.py` - Tema B: logging CSV pentru Braitenberg
- `tema/tema_b_grafice.py` - Tema B: generare grafice PNG din CSV
- `tema/tema_c_explorer.py` - Tema C: explorer autonom 60s
- `tema/tema_d_bonus_iubire.py` - Tema D: Braitenberg "Iubire" (bonus)
- `tema/README.md` - detalii specifice fiecarei teme

## 2. Cerinte software

- Python 3.10+
- CoppeliaSim deschis cu scena `pioneer_lab06.ttt`
- Simularea pornita (Play) in CoppeliaSim

Dependinte Python (fisier: `requirements.txt`):
- `coppeliasim-zmqremoteapi-client`
- `matplotlib`

## 3. Instalare rapida (Windows PowerShell)

```powershell
cd lab06
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Rulare cerinte 3.1-3.6

Din folderul `lab06`:

```powershell
python .\cerinta_3_1_conectare.py
python .\cerinta_3_2_patrat.py
python .\cerinta_3_3_senzori.py
python .\cerinta_3_4_stop_obstacol.py
python .\cerinta_3_5_braitenberg.py
python .\cerinta_3_6_wall_following.py
```

## 5. Rulare teme

Din folderul `lab06\tema`:

```powershell
python .\tema_a_recuperare.py
python .\tema_b_logging.py
python .\tema_b_grafice.py
python .\tema_c_explorer.py
python .\tema_d_bonus_iubire.py
```

### 5.1 Cum verifici temele (subpunct)

Inainte de verificare:
- deschide CoppeliaSim cu scena `pioneer_lab06.ttt`;
- porneste simularea (Play);
- evita rularea simultana a altor scripturi care controleaza motoarele robotului.

Verificare Tema A:
- ruleaza `tema_a_recuperare.py`;
- confirma in consola tranzitiile `FORWARD -> BACKWARD -> TURNING -> FORWARD`;
- pune un obstacol in fata robotului si verifica faptul ca nu ramane blocat permanent.

Verificare Tema B:
- ruleaza `tema_b_logging.py` pentru 20-60s, apoi opreste cu Ctrl+C;
- verifica existenta fisierului `tema/tema_b_log_braitenberg.csv`;
- ruleaza `tema_b_grafice.py`;
- verifica generarea imaginilor:
	- `tema/tema_b_traseu_xy.png`
	- `tema/tema_b_viteze_timp.png`
	- `tema/tema_b_heatmap_senzori.png`

Verificare Tema C:
- ruleaza `tema_c_explorer.py`;
- confirma rularea minima de 60s si comportamentul de explorare (wall-follow + recuperare la blocaj);
- verifica fisierele rezultate:
	- `tema/tema_c_traseu.csv`
	- `tema/tema_c_traseu.png`

Verificare Tema D:
- ruleaza `tema_d_bonus_iubire.py`;
- plaseaza obstacole/stimuli in fata robotului;
- confirma ca robotul se orienteaza spre stimul si incetineste cand este aproape.




 1. Setup o singură dată

În CoppeliaSim:
Open Scene și încarci scena pioneer_lab06.ttt
Verifici că robotul PioneerP3DX este prezent
Pentru teste curate, dezactivezi scriptul intern Braitenberg al robotului (ca să nu se bată cu scripturile tale externe):
Click dreapta pe PioneerP3DX
Edit child script
Disable script (sau comentezi controlul motoarelor)
Apeși Play în simulator înainte să rulezi scripturile Python
În PowerShell:
Dacă nu ai mediu virtual:
python -m venv .venv
Activare:
.venv\Scripts\activate

Instalare:
pip install -r .\requirements.txt

2. Ce rulezi pentru fiecare temă și ce trebuie să vezi

Tema A
Rulezi: python tema_a_recuperare.py
Fișier: tema_a_recuperare.py
Ce verifici:
Robotul merge înainte
Când întâlnește obstacol: dă înapoi ~1s, virează stânga/dreapta, apoi reia mersul
În consolă vezi stări FORWARD, BACKWARD, TURNING
Test în Coppelia:
Pune o cutie în fața robotului și vezi că nu rămâne blocat


Tema B
Pas 1: rulezi logging
python tema_b_logging.py
Fișier: tema_b_logging.py
Lași 20-60 secunde, apoi Ctrl+C

Pas 2: generezi grafice
python tema_b_grafice.py
Fișier: tema_b_grafice.py
Ce verifici:
există CSV: lab06/tema/tema_b_log_braitenberg.csv
există PNG-uri:
lab06/tema/tema_b_traseu_xy.png
lab06/tema/tema_b_viteze_timp.png
lab06/tema/tema_b_heatmap_senzori.png


Tema C
Rulezi: python tema_c_explorer.py
Fișier: tema_c_explorer.py
Ce verifici:
rulează minim 60 secunde
urmărește pereți, evită obstacole și se recuperează dacă se blochează
la final salvează:
lab06/tema/tema_c_traseu.csv
lab06/tema/tema_c_traseu.png
În Coppelia:
pregătește arenă cu mai multe obstacole
pornește screen recording pentru cerința video (din OS sau din Coppelia)


Tema D
Rulezi: python tema_d_bonus_iubire.py
Fișier: tema_d_bonus_iubire.py
Ce verifici:
cu stimul frontal/lateral, robotul se orientează spre el
când se apropie, încetinește
în consolă vezi activări aL/aR și viteze vL/vR


3. Config minim în Coppelia pentru test corect

Simularea pe Play înainte de script
Obstacole plasate la distanțe rezonabile (0.3-1.0m de robot)
Fără alte scripturi active care setează aceleași motoare
Dacă ceva pare blocat:
Stop simulation
Repositionare robot
Play din nou
rerulare script

## 6. Artefacte generate

Tema B:
- `tema/tema_b_log_braitenberg.csv`
- `tema/tema_b_traseu_xy.png`
- `tema/tema_b_viteze_timp.png`
- `tema/tema_b_heatmap_senzori.png`

Tema C:
- `tema/tema_c_traseu.csv`
- `tema/tema_c_traseu.png`

## 7. Observatii

- Daca apare eroare de tip conexiune (`ConnectionRefusedError`), verifica faptul ca CoppeliaSim este pornit si simularea este activa.
- Daca editorul afiseaza importuri nerezolvate pentru `coppeliasim_zmqremoteapi_client`, instaleaza dependintele in mediul virtual activ.
- Pentru tema C, cerinta video se realizeaza prin screen recording in timpul executiei scriptului.
