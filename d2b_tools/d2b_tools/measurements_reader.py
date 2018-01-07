#!/usr/bin/env python
'''
Class to read the D2B data files.

We want to read all the measurement files into a set of measurements.
Each measurment will have it's 128 counts, the angular position of the reading, the detector number and the monitor value.

We represent the detectors as:
* Detector 0 is the rightmost detector, detector 127 is the leftmost one.
* Pixel 0 is the lowest pixel and pixel 127 is the hightest one.

This code asumes that the count information is writen is shown in the following
diagram:

16384   \/<<<<<<<^        <<<^
^       \/       ^           ^
^       \/       ^           ^
   .                   .
   .                   .
   .                   .
^       \/       ^   ....    ^
^       \/       ^           ^
^<<<<<<<\/       ^<<<        0

The first number is the count reading of the lowest pixel of the rightmost detector.
The last number is the highest reading of the leftmost detector.

'''

import math


def pixel_per_detector_generator(all_counts, pixel_amount):
    '''
    Reads all the counts and returns a series of lists, each list of pixel_amount length

    :param all_counts: All the counts of the measurement (128 detectors * 128 pixels per detector)
    :param pixel_amount: The number of pixels per detector (all detectors have the same number of pixels)
    '''
    for detector in range(0, len(all_counts), pixel_amount):
        pixels = all_counts[detector:detector + pixel_amount]
        if detector%2 != 0:
            pixels.reverse()
        yield pixels


def get_metadata(segment_header_separator, segment):
    header = segment.split(segment_header_separator)[0]
    names, values = header.split('\n')[4:6]
    names = names.replace('Total Cou', 'Total_Cou')
    return dict(zip(names.split(), [float(val) for val in values.split()]))


def get_counts(segment_header_separator, rightmost_angle, segment):
    counts_string = segment.split(segment_header_separator)[1]
    counts_string = counts_string.replace('\n', ' ')
    all_counts = [int(val) for val in counts_string.split()]
    pixel_and_detector_amount = int(math.sqrt(all_counts[0]))
    return list(pixel_per_detector_generator(all_counts[2:], pixel_and_detector_amount))



class DetectorMeasurement:

    SEGMENT_HEADER_SEPARATOR = 'I'*80

    # :param detector_angle_calibration: Angular distance from the rightmost detector to every detector.
    #     The list should have 128 values, with the last value being 0.


    @property
    def rightmost_angle(self):
        return self._metadata['anglesx1000']

    @classmethod
    def from_measurement_string(segment_string):
        measurement = DetectorMeasurement()
        measurement._metadata = get_metadata(self.SEGMENT_HEADER_SEPARATOR, segment_string)
        measurement._counts = get_counts(self.SEGMENT_HEADER_SEPARATOR, segment_string, measurement.rightmost_angle)
        return measurement

    def get_detector_angle(self, detector_number):
        return self.rightmost_angle - self.detector_angle_calibration[detector_number]

class MeasurementsReader:

    SEPARATOR_STRING = 'S'*80
    SEGMENTS_TO_SKIP = 1

    def get_measurments_segments(self, file_data):
        return file_data.split(self.SEPARATOR_STRING)[self.SEGMENTS_TO_SKIP:]

    def read_file(self, file_name):
        return [0]*25
