"""
Tema B - Braitenberg cu inregistrare de date in CSV.
Salveaza: timestamp, v_left, v_right, s0..s7, pos_x, pos_y
"""
import csv
import os
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

V_BASE = 3.0
V_MAX = 6.0
K_SENSOR = 6.0
SENSOR_MAX = 1.0
DT = 0.05

WEIGHTS = [
    (+0.5, -0.5),
    (+1.0, -1.0),
    (+1.5, -1.5),
    (+2.0, -2.0),
    (-2.0, +2.0),
    (-1.5, +1.5),
    (-1.0, +1.0),
    (-0.5, +0.5),
]


def clamp(value, low, high):
    return max(low, min(high, value))


def read_front_proximities(sim, sensors):
    values = []
    for i in range(8):
        result, distance, *_ = sim.readProximitySensor(sensors[i])
        if result:
            proximity = 1.0 - (distance / SENSOR_MAX)
            values.append(clamp(proximity, 0.0, 1.0))
        else:
            values.append(0.0)
    return values


def braitenberg_velocities(sensor_proximities):
    v_left = V_BASE
    v_right = V_BASE

    for i, (w_l, w_r) in enumerate(WEIGHTS):
        s_i = sensor_proximities[i]
        v_left += K_SENSOR * w_l * s_i
        v_right += K_SENSOR * w_r * s_i

    v_left = clamp(v_left, -V_MAX, V_MAX)
    v_right = clamp(v_right, -V_MAX, V_MAX)
    return v_left, v_right


def main():
    client = RemoteAPIClient()
    sim = client.require('sim')

    robot = sim.getObject('/PioneerP3DX')
    left_motor = sim.getObject('/PioneerP3DX/leftMotor')
    right_motor = sim.getObject('/PioneerP3DX/rightMotor')
    sensors = [sim.getObject(f'/PioneerP3DX/ultrasonicSensor[{i}]') for i in range(16)]

    out_dir = os.path.dirname(__file__)
    out_csv = os.path.join(out_dir, 'tema_b_log_braitenberg.csv')

    fieldnames = ['timestamp', 'v_left', 'v_right']
    fieldnames += [f's{i}' for i in range(8)]
    fieldnames += ['pos_x', 'pos_y']

    sim.startSimulation()
    print(f"Tema B pornita. Logging in: {out_csv}")

    try:
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            iteration = 0
            while True:
                s = read_front_proximities(sim, sensors)
                v_left, v_right = braitenberg_velocities(s)

                sim.setJointTargetVelocity(left_motor, v_left)
                sim.setJointTargetVelocity(right_motor, v_right)

                pos = sim.getObjectPosition(robot, sim.handle_world)
                row = {
                    'timestamp': sim.getSimulationTime(),
                    'v_left': v_left,
                    'v_right': v_right,
                    'pos_x': pos[0],
                    'pos_y': pos[1],
                }
                for i in range(8):
                    row[f's{i}'] = s[i]
                writer.writerow(row)

                if iteration % 20 == 0:
                    print(f"t={row['timestamp']:.2f}s vL={v_left:+.2f} vR={v_right:+.2f}")

                iteration += 1
                time.sleep(DT)

    except KeyboardInterrupt:
        print("\nStop manual. CSV salvat.")
    finally:
        sim.setJointTargetVelocity(left_motor, 0.0)
        sim.setJointTargetVelocity(right_motor, 0.0)
        sim.stopSimulation()


if __name__ == '__main__':
    main()
