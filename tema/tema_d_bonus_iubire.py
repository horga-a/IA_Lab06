"""
Tema D (Bonus) - Braitenberg "Iubire".
Conexiuni ipsilaterale inhibitorii: stimul pe o parte reduce viteza rotii de pe aceeasi parte.
Efect: robotul se orienteaza spre stimul si incetineste cand ajunge aproape.
"""
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

V_BASE = 3.0
K_INHIBIT = 3.0
SENSOR_MAX = 1.0
DT = 0.05

LEFT_FRONT = [0, 1, 2, 3]
RIGHT_FRONT = [4, 5, 6, 7]


def clamp(value, low, high):
    return max(low, min(high, value))


def side_activation(sim, sensors, indices):
    acc = 0.0
    for idx in indices:
        result, distance, *_ = sim.readProximitySensor(sensors[idx])
        if result:
            proximity = 1.0 - (distance / SENSOR_MAX)
            acc += clamp(proximity, 0.0, 1.0)
    return acc / max(1, len(indices))


def main():
    client = RemoteAPIClient()
    sim = client.require('sim')

    left_motor = sim.getObject('/PioneerP3DX/leftMotor')
    right_motor = sim.getObject('/PioneerP3DX/rightMotor')
    sensors = [sim.getObject(f'/PioneerP3DX/ultrasonicSensor[{i}]') for i in range(16)]

    sim.startSimulation()
    print('Tema D (Iubire) pornita. Ctrl+C pentru oprire.')

    try:
        iteration = 0
        while True:
            a_left = side_activation(sim, sensors, LEFT_FRONT)
            a_right = side_activation(sim, sensors, RIGHT_FRONT)

            # Iubire: conexiune ipsilaterala inhibitoare
            v_left = V_BASE - K_INHIBIT * a_left
            v_right = V_BASE - K_INHIBIT * a_right

            # Cand ambele activari sunt mari, robotul incetineste aproape de stimul
            v_left = clamp(v_left, 0.0, V_BASE)
            v_right = clamp(v_right, 0.0, V_BASE)

            sim.setJointTargetVelocity(left_motor, v_left)
            sim.setJointTargetVelocity(right_motor, v_right)

            if iteration % 20 == 0:
                print(
                    f"aL={a_left:.2f} aR={a_right:.2f} | "
                    f"vL={v_left:.2f} vR={v_right:.2f}"
                )
            iteration += 1
            time.sleep(DT)

    except KeyboardInterrupt:
        print('\nStop manual.')
    finally:
        sim.setJointTargetVelocity(left_motor, 0.0)
        sim.setJointTargetVelocity(right_motor, 0.0)
        sim.stopSimulation()


if __name__ == '__main__':
    main()
