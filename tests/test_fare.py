# tests/test_fare.py

import unittest
from main import calculate_fare


class TestCalculateFare(unittest.TestCase):
    """
    Conjunto de pruebas para la función calculate_fare.
    """

    def test_calculate_fare_only_stopped(self):
        """
        Si el taxi solo está parado, la tarifa debe ser
        segundos_parado * 0.02.
        """
        # Arrange (preparar datos)
        seconds_stopped = 10  # 10 segundos parado
        seconds_moving = 0    # 0 en movimiento

        # Act (ejecutar la función que queremos probar)
        result = calculate_fare(seconds_stopped, seconds_moving)

        # Assert (comprobar el resultado)
        self.assertAlmostEqual(result, 0.20)

    def test_calculate_fare_only_moving(self):
        """
        Si el taxi solo está en movimiento, la tarifa debe ser
        segundos_movimiento * 0.05.
        """
        seconds_stopped = 0
        seconds_moving = 10  # 10 segundos en movimiento

        result = calculate_fare(seconds_stopped, seconds_moving)

        self.assertAlmostEqual(result, 0.50)

    def test_calculate_fare_mixed(self):
        """
        Si el taxi está parte parado y parte en movimiento,
        la tarifa es la suma de ambos.
        """
        seconds_stopped = 10   # 10 * 0.02 = 0.20
        seconds_moving = 20    # 20 * 0.05 = 1.00

        result = calculate_fare(seconds_stopped, seconds_moving)

        self.assertAlmostEqual(result, 1.20)


if __name__ == "__main__":
    unittest.main()
