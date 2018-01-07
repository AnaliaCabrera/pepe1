import unittest

from d2b_tools import measurements_reader


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self._mr = measurements_reader.MeasurementsReader()

    def read_sample_segment(self, segment_index=0):
        with open('data/sample_input.txt', 'r') as infile:
            file_data = infile.read()
            segments = self._mr.get_measurments_segments(file_data)
        return segments[segment_index]

    def test_get_metadata(self):
        segment = self.read_sample_segment()
        metadata = measurements_reader.get_metadata(measurements_reader.Shot.SEGMENT_HEADER_SEPARATOR,
                                                    segment)
        self.assertTrue('Total_Cou' in metadata)
        self.assertTrue('monitor' in metadata)
        self.assertTrue('anglesx1000' in metadata)
        self.assertTrue('time' in metadata)
        self.assertAlmostEqual(metadata['monitor'], 5e+5, 10)

    def test_get_counts(self):
        segment = self.read_sample_segment()
        counts = measurements_reader.get_counts(measurements_reader.Shot.SEGMENT_HEADER_SEPARATOR,
                                                1.31246000e5, segment)
        self.assertEqual(len(counts), 128)
        self.assertEqual(len(counts[0]), 128)

    def test_pixel_per_detector_generator(self):
        test_list = [0,1,2,5,4,3,6,7,8,11,10,9]
        output = list(measurements_reader.pixel_per_detector_generator(test_list, 3))
        self.assertListEqual(output, [[0,1,2], [3,4,5], [6,7,8], [9,10,11]])


class TestShot(unittest.TestCase):

    def test_default(self):
        s = measurements_reader.Shot({})
        self.assertEqual(len(s._detectors), 0)
        self.assertEqual(len(s._detector_angle_calibration), 128)

    def test_rightmost_angle(self):
        s = measurements_reader.Shot({'anglesx1000': 2})
        self.assertEqual(s.rightmost_angle, 2)

    def test_monitor(self):
        s = measurements_reader.Shot({'monitor': 5e5})
        self.assertAlmostEqual(s.monitor, 5e5, 10)

    def test_add_detector_measurment(self):
        s = measurements_reader.Shot({'anglesx1000': 0, 'monitor': 5e5})
        s.add_detector_measurement(0, [0, 1, 2])
        detectors = s.get_detector_measurments()
        self.assertEqual(len(detectors), 1)
        self.assertAlmostEqual(detectors[0]._monitor, 5e5, 10)
        self.assertEqual(detectors[0]._number, 0)

class TestMeasurementReader(unittest.TestCase):

    def setUp(self):
        self.mr_ = measurements_reader.MeasurementsReader()

    def read_sample_file(self, segment_index=0):
        with open('data/sample_input.txt', 'r') as infile:
            file_data = infile.read()
            segments = self.mr_.get_measurments_segments(file_data)
        return segments

    def test_get_measurments_segments(self):
        segments = self.read_sample_file()
        self.assertEqual(len(segments), 25)
        for segment in segments:
            self.assertTrue(any(['I'*80 in line for line in segment.split('\n')]))

    def test_read_file(self):
        measurements = self.mr_.read_file('data/sample_input.txt')
        self.assertEqual(len(measurements), 25)



if __name__ == '__main__':
    unittest.main()
