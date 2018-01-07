import unittest

from d2b_tools import measurements_reader


class TestDetectorMeasurement(unittest.TestCase):

    def setUp(self):
        self._mr = measurements_reader.MeasurementsReader()

    def read_sample_segment(self, segment_index=0):
        with open('data/sample_input.txt', 'r') as infile:
            file_data = infile.read()
            segments = self._mr.get_measurments_segments(file_data)
        return segments[segment_index]


    def test_get_metadata(self):
        segment = self.read_sample_segment()
        metadata = measurements_reader.get_metadata(measurements_reader.DetectorMeasurement.SEGMENT_HEADER_SEPARATOR,
                                                    segment)
        self.assertTrue('Total_Cou' in metadata)
        self.assertTrue('monitor' in metadata)
        self.assertTrue('anglesx1000' in metadata)
        self.assertTrue('time' in metadata)
        self.assertAlmostEqual(metadata['monitor'], 5e+5, 10)

    def test_get_counts(self):
        segment = self.read_sample_segment()
        counts = measurements_reader.get_counts(measurements_reader.DetectorMeasurement.SEGMENT_HEADER_SEPARATOR,
                                                1.31246000e5, segment)
        self.assertEqual(len(counts), 128)
        self.assertEqual(len(counts[0]), 128)

    def test_pixel_per_detector_generator(self):
        test_list = [0,1,2,5,4,3,6,7,8,11,10,9]
        output = list(measurements_reader.pixel_per_detector_generator(test_list, 3))
        self.assertListEqual(output, [[0,1,2], [3,4,5], [6,7,8], [9,10,11]])


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
