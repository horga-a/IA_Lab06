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
