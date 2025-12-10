import unittest
import os
from history import save_trip_to_history

class TestHistory(unittest.TestCase):

    def setUp(self):
        """
        Antes de cada test: creamos un archivo temporal.
        """
        self.test_file = "test_history.txt"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def tearDown(self):
        """ Despues del test:borramos el archivo temporal."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_trip_to_history_writes_line(self):
        stopped = 10.0
        moving = 20.0
        total = 5.50

        save_trip_to_history(stopped, moving, total, filename=self.test_file)

        with open(self.test_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Verificamos que los elementos correctos están en la línea 

        self.assertIn("stopped=10.0s", content)
        self.assertIn("moving=20.0s", content)
        self.assertIn ("fare=5.50€", content)

if __name__ == "__main__":
    unittest.main()