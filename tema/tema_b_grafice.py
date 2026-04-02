"""
Tema B - Generare grafice din CSV-ul logat de tema_b_logging.py
Output:
- tema_b_traseu_xy.png
- tema_b_viteze_timp.png
- tema_b_heatmap_senzori.png
"""
import csv
import os

import matplotlib.pyplot as plt


def load_csv(path):
    timestamps = []
    v_left = []
    v_right = []
    pos_x = []
    pos_y = []
    sensor_matrix = []

    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(float(row['timestamp']))
            v_left.append(float(row['v_left']))
            v_right.append(float(row['v_right']))
            pos_x.append(float(row['pos_x']))
            pos_y.append(float(row['pos_y']))
            sensor_matrix.append([float(row[f's{i}']) for i in range(8)])

    return timestamps, v_left, v_right, pos_x, pos_y, sensor_matrix


def main():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, 'tema_b_log_braitenberg.csv')

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Nu exista fisierul: {csv_path}")

    t, v_l, v_r, x, y, sensors = load_csv(csv_path)

    # 1) Traiectorie XY
    plt.figure(figsize=(7, 6))
    plt.plot(x, y, linewidth=1.5)
    plt.scatter([x[0]], [y[0]], c='green', label='start')
    plt.scatter([x[-1]], [y[-1]], c='red', label='stop')
    plt.title('Tema B - Traiectoria robotului (XY)')
    plt.xlabel('pos_x [m]')
    plt.ylabel('pos_y [m]')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.legend()
    out1 = os.path.join(base_dir, 'tema_b_traseu_xy.png')
    plt.tight_layout()
    plt.savefig(out1, dpi=140)
    plt.close()

    # 2) Viteze in timp
    plt.figure(figsize=(9, 4.8))
    plt.plot(t, v_l, label='v_left')
    plt.plot(t, v_r, label='v_right')
    plt.title('Tema B - Viteze roti in timp')
    plt.xlabel('t [s]')
    plt.ylabel('viteza [rad/s]')
    plt.grid(True, alpha=0.3)
    plt.legend()
    out2 = os.path.join(base_dir, 'tema_b_viteze_timp.png')
    plt.tight_layout()
    plt.savefig(out2, dpi=140)
    plt.close()

    # 3) Heatmap senzori (s0..s7 pe axa Y, timp pe axa X)
    sensor_rows = [[sample[i] for sample in sensors] for i in range(8)]

    plt.figure(figsize=(10, 4.8))
    plt.imshow(sensor_rows, aspect='auto', interpolation='nearest', origin='lower')
    plt.colorbar(label='activare senzor [0..1]')
    plt.yticks(range(8), [f's{i}' for i in range(8)])
    plt.title('Tema B - Heatmap activare senzori frontali')
    plt.xlabel('esantion timp')
    plt.ylabel('senzor')
    out3 = os.path.join(base_dir, 'tema_b_heatmap_senzori.png')
    plt.tight_layout()
    plt.savefig(out3, dpi=140)
    plt.close()

    print('Grafice generate:')
    print(out1)
    print(out2)
    print(out3)


if __name__ == '__main__':
    main()
