# Tema A, B, C, D - Implementari

## Tema A - Evitare cu recuperare

Fisier: `tema_a_recuperare.py`

Comportament:
- `FORWARD`: robotul merge inainte pana detecteaza obstacol frontal sub pragul `STOP_DISTANCE`.
- `BACKWARD`: robotul da inapoi `BACKWARD_TIME` secunde.
- `TURNING`: robotul vireaza aleator stanga/dreapta aproximativ 90 grade timp de `TURN_TIME`.
- Dupa `TURNING`, revine in `FORWARD`.

## Tema B - Braitenberg cu inregistrare de date

Fisiere:
- `tema_b_logging.py`
- `tema_b_grafice.py`

Pasii de rulare:
1. Ruleaza `tema_b_logging.py` cat timp doresti sa colectezi date.
2. Opreste cu Ctrl+C (se salveaza `tema_b_log_braitenberg.csv`).
3. Ruleaza `tema_b_grafice.py` pentru a genera:
	- `tema_b_traseu_xy.png`
	- `tema_b_viteze_timp.png`
	- `tema_b_heatmap_senzori.png`

CSV contine coloanele cerute: `timestamp`, `v_left`, `v_right`, `s0`..`s7`, `pos_x`, `pos_y`.

## Tema C - Robot Explorer

Fisier: `tema_c_explorer.py`

Caracteristici:
- combina wall-following cu recuperare (`BACKWARD` + `TURNING`);
- detecteaza blocaj local pe fereastra temporala (`STUCK_WINDOW`);
- ruleaza implicit minim 60 secunde (`DURATION_SEC = 60.0`);
- salveaza traseul in `tema_c_traseu.csv`;
- genereaza graficul `tema_c_traseu.png`.

Pentru cerinta video, foloseste captura ecran CoppeliaSim in timpul rularii scriptului.

## Tema D - Braitenberg "Iubire" (Bonus)

Fisier: `tema_d_bonus_iubire.py`

Model implementat:
- conexiuni ipsilaterale inhibitorii (stimul stanga inhiba motor stanga, stimul dreapta inhiba motor dreapta);
- robotul se orienteaza spre stimul si reduce viteza cand este foarte aproape.

Diferenta fata de "Frica":
- "Frica" (tema 3.5) se indeparteaza de obstacol/stimul;
- "Iubire" se apropie de stimul, apoi incetineste.
