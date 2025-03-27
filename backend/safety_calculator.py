import numpy as np

class SafetyCalculator:
    @staticmethod
    def calculate_gas_emission(v, q_extraction):
        return 0.25 * v**2 + 1.8 * v - 0.05 * q_extraction + 2.1

    @staticmethod
    def calculate_gas_concentration(Q, q_airflow):
        return (Q / q_airflow) * 100

    @staticmethod
    def find_safe_speed(q_airflow, q_extraction, max_speed=5.0, step=0.1):
        safe_speed = 0.0
        for v in np.arange(0, max_speed + step, step):
            Q = 0.25 * v**2 + 1.8 * v - 0.05 * q_extraction + 2.1
            if (Q / q_airflow) <= 0.01:
                safe_speed = v
            else:
                break
        return round(safe_speed, 1)