"""
Tema C - Robot Explorer.
Combina wall-following cu recuperare la blocaj pentru explorare autonoma.
Ruleaza implicit 60s si salveaza traiectoria + grafic.
"""
import csv
import os
import random
import time
from enum import Enum

import matplotlib.pyplot as plt
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

V_BASE = 2.0
TARGET_DIST = 0.4
K_P = 3.0
FRONT_STOP = 0.40
SENSOR_MAX = 1.0

RIGHT_SENSORS = [8, 9]
FRONT_SENSORS = [3, 4]

DURATION_SEC = 60.0
DT = 0.05

BACKWARD_TIME = 1.0
TURN_TIME = 1.6
STUCK_WINDOW = 2.5
STUCK_MIN_MOV = 0.03


class ExplorerState(Enum):
    WALL_FOLLOW = 'WALL_FOLLOW'
    BACKWARD = 'BACKWARD'
    TURNING = 'TURNING'


def clamp(value, low, high):
    return max(low, min(high, value))


def read_min_dist(sim, sensors, indices):
    min_dist = SENSOR_MAX
    for idx in indices:
        result, dist, *_ = sim.readProximitySensor(sensors[idx])
        if result and dist < min_dist:
            min_dist = dist
    return min_dist


def set_speed(sim, lm, rm, vl, vr):
    sim.setJointTargetVelocity(lm, vl)
    sim.setJointTargetVelocity(rm, vr)


def distance_2d(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return (dx * dx + dy * dy) ** 0.5


def main():
    client = RemoteAPIClient()
    sim = client.require('sim')

    robot = sim.getObject('/PioneerP3DX')
    left_motor = sim.getObject('/PioneerP3DX/leftMotor')
    right_motor = sim.getObject('/PioneerP3DX/rightMotor')
    sensors = [sim.getObject(f'/PioneerP3DX/ultrasonicSensor[{i}]') for i in range(16)]

    out_dir = os.path.dirname(__file__)
    csv_path = os.path.join(out_dir, 'tema_c_traseu.csv')
    png_path = os.path.join(out_dir, 'tema_c_traseu.png')

    state = ExplorerState.WALL_FOLLOW
    state_until = 0.0
    turn_dir = 1

    trace = []
    history = []

    sim.startSimulation()
    print(f"Tema C pornita. Explorare timp de {DURATION_SEC:.0f}s.")

    t0 = time.time()
    try:
        while True:
            elapsed = time.time() - t0
            if elapsed >= DURATION_SEC:
                print('Durata minima 60s atinsa.')
                break

            sim_t = sim.getSimulationTime()
            pos = sim.getObjectPosition(robot, sim.handle_world)
            trace.append((sim_t, pos[0], pos[1]))

            history.append((sim_t, pos[0], pos[1]))
            while history and (sim_t - history[0][0]) > STUCK_WINDOW:
                history.pop(0)

            dist_front = read_min_dist(sim, sensors, FRONT_SENSORS)
            dist_right = read_min_dist(sim, sensors, RIGHT_SENSORS)

            is_stuck = False
            if len(history) >= 2:
                moved = distance_2d(history[-1], history[0])
                is_stuck = moved < STUCK_MIN_MOV and dist_front < FRONT_STOP + 0.05

            if state == ExplorerState.WALL_FOLLOW and (dist_front < FRONT_STOP or is_stuck):
                state = ExplorerState.BACKWARD
                state_until = sim_t + BACKWARD_TIME

            if state == ExplorerState.BACKWARD:
                set_speed(sim, left_motor, right_motor, -1.5, -1.5)
                if sim_t >= state_until:
                    state = ExplorerState.TURNING
                    state_until = sim_t + TURN_TIME
                    turn_dir = random.choice([-1, 1])

            elif state == ExplorerState.TURNING:
                if turn_dir > 0:
                    set_speed(sim, left_motor, right_motor, -2.2, +2.2)
                else:
                    set_speed(sim, left_motor, right_motor, +2.2, -2.2)

                if sim_t >= state_until:
                    state = ExplorerState.WALL_FOLLOW

            else:
                if dist_right >= SENSOR_MAX * 0.95:
                    v_left, v_right = V_BASE, V_BASE * 0.5
                else:
                    error = dist_right - TARGET_DIST
                    v_left = V_BASE + K_P * error
                    v_right = V_BASE - K_P * error
                    cap = V_BASE * 1.6
                    v_left = clamp(v_left, -cap, cap)
                    v_right = clamp(v_right, -cap, cap)
                set_speed(sim, left_motor, right_motor, v_left, v_right)

            if int(elapsed / 2.0) != int((elapsed - DT) / 2.0):
                print(f"t={elapsed:5.1f}s state={state.value:<11} front={dist_front:.3f} right={dist_right:.3f}")

            time.sleep(DT)

    except KeyboardInterrupt:
        print('\nStop manual. Salvez rezultate partiale.')
    finally:
        set_speed(sim, left_motor, right_motor, 0.0, 0.0)
        sim.stopSimulation()

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'pos_x', 'pos_y'])
        writer.writerows(trace)

    if trace:
        xs = [p[1] for p in trace]
        ys = [p[2] for p in trace]
        plt.figure(figsize=(7, 6))
        plt.plot(xs, ys, linewidth=1.3)
        plt.scatter([xs[0]], [ys[0]], c='green', label='start')
        plt.scatter([xs[-1]], [ys[-1]], c='red', label='stop')
        plt.title('Tema C - Traiectorie explorer (XY)')
        plt.xlabel('X [m]')
        plt.ylabel('Y [m]')
        plt.axis('equal')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_path, dpi=140)
        plt.close()

    print('Rezultate salvate:')
    print(csv_path)
    print(png_path)


if __name__ == '__main__':
    main()
