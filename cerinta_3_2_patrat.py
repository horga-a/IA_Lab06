"""
Cerinta 3.2 - Controlul motorului: miscare in patrat (bucla deschisa).
"""
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

V_FORWARD = 2.0
V_TURN = 2.0
T_LINIE = 3.0
T_VIRAJ = 1.57


def set_velocity(sim, left_motor, right_motor, v_left, v_right):
    sim.setJointTargetVelocity(left_motor, v_left)
    sim.setJointTargetVelocity(right_motor, v_right)


def move_forward(sim, left_motor, right_motor, duration):
    set_velocity(sim, left_motor, right_motor, V_FORWARD, V_FORWARD)
    time.sleep(duration)


def turn_left_90(sim, left_motor, right_motor):
    set_velocity(sim, left_motor, right_motor, -V_TURN, V_TURN)
    time.sleep(T_VIRAJ)


def stop(sim, left_motor, right_motor):
    set_velocity(sim, left_motor, right_motor, 0.0, 0.0)


def main():
    client = RemoteAPIClient()
    sim = client.require('sim')

    robot = sim.getObject('/PioneerP3DX')
    left_motor = sim.getObject('/PioneerP3DX/leftMotor')
    right_motor = sim.getObject('/PioneerP3DX/rightMotor')

    sim.startSimulation()
    print("Simulare pornita. Robotul va parcurge un patrat.")
    time.sleep(0.5)

    try:
        for latura in range(4):
            print(f"Latura {latura + 1}/4 - mers inainte {T_LINIE}s")
            move_forward(sim, left_motor, right_motor, T_LINIE)
            print("Viraj stanga ~90 deg")
            turn_left_90(sim, left_motor, right_motor)

        stop(sim, left_motor, right_motor)
        pos = sim.getObjectPosition(robot, sim.handle_world)
        print(f"\nPozitie finala: X={pos[0]:.3f} m, Y={pos[1]:.3f} m")
        print("(Ideal: aproape de pozitia initiala)")
        time.sleep(1.0)
    finally:
        stop(sim, left_motor, right_motor)
        sim.stopSimulation()
        print("Simulare oprita.")


if __name__ == '__main__':
    main()
