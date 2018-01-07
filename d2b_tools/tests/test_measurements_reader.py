import unittest
from d2b_tools import measurements_reader


class TestMeasurementReader(unittest.TestCase):

    def setUp(self):
        self.mr = measurement_reader.MeasurementsReader()


if __name__ == '__main__':
    unittest.main()
