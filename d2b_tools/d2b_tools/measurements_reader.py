#!/usr/bin/env python
'''
Class to read the D2B data files.

We want to read all the measurement files into a set of measurements.
Each measurment will have it's 128 counts, the angular position of the reading, the detector number and the monitor value.

We represent the detectors as:
* Detector 0 is the rightmost detector, detector 127 is the leftmost one.
* Pixel 0 is the lowest pixel and pixel 127 is the hightest one.

This code assumes that the count information is written is shown in the following
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
import argparse
import math
import os
import pickle

DEFAULT_CALIBRATION = [-158.750, -157.500, -156.250, -155.000, -153.750, -152.500,
                       -151.250, -150.000, -148.750, -147.500, -146.250, -145.000,
                       -143.750, -142.500, -141.250, -140.000, -138.750, -137.500,
                       -136.250, -135.000, -133.750, -132.500, -131.262, -130.027,
                       -128.764, -127.501, -126.262, -124.986, -123.744, -122.488,
                       -121.250, -119.996, -118.749, -117.503, -116.240, -115.000,
                       -113.760, -112.510, -111.225, -110.011, -108.726, -107.537,
                       -106.240, -104.974, -103.739, -102.491, -101.254, -99.9934,
                       -98.7551, -97.5007, -96.2569, -94.9937, -93.7413, -92.5081,
                       -91.2396, -89.9824, -88.7602, -87.5170, -86.2329, -84.9932,
                       -83.7641, -82.5050, -81.2662, -79.9966, -78.7527, -77.5035,
                       -76.2564, -74.9872, -73.7477, -72.5086, -71.2457, -70.0003,
                       -68.7467, -67.4861, -66.2499, -65.0244, -63.7557, -62.5025,
                       -61.2484, -59.9862, -58.7416, -57.4992, -56.2372, -54.9913,
                       -53.7547, -52.4989, -51.2399, -50.0088, -48.7492, -47.4948,
                       -46.2517, -45.0034, -43.7366, -42.4932, -41.2465, -39.9866,
                       -38.7377, -37.5183, -36.2678, -35.0202, -33.7731, -32.4958,
                       -31.2734, -30.0018, -28.7291, -27.4887, -26.2319, -24.9728,
                       -23.7554, -22.4771, -21.2376, -20.0052, -18.7470, -17.5007,
                       -16.2531, -14.9891, -13.7492, -12.5056, -11.2798, -10.0067,
                       -8.73692, -7.50000, -6.25000, -5.00000, -3.75000, -2.50000,
                       -1.25000, 0.000000]


def pixel_per_detector_generator(all_counts, pixel_amount):
    '''
    Reads all the counts and returns a series of lists, each list of pixel_amount length

    :param all_counts: All the counts of the measurement (128 detectors * 128 pixels per detector)
    :param pixel_amount: The number of pixels per detector (all detectors have the same number of pixels)
    '''
    for first_pixel in range(0, len(all_counts), pixel_amount):
        pixels = all_counts[first_pixel:first_pixel + pixel_amount]
        if int(first_pixel/pixel_amount)%2 == 0:
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


class Detector:

    def __init__(self, number, monitor, angle, counts):
        self.number = number
        self.angle = angle
        self.counts = counts
        self.monitor = monitor

    def __str__(self):
        '''
        This method wive a format to a return of this class
        ATENTION self._counts have the counts for each pixel but we show only the length of this counts that is equivalent at the number of pixel
        '''
        return 'Detector {}, at angle {}, with monitor {} has {} counts'.format(self.number,
                                                                                self.angle,
                                                                                self.monitor,
                                                                                len(self.counts))

class Shot:

    SEGMENT_HEADER_SEPARATOR = 'I'*80

    @property
    def rightmost_angle(self):
        return self._metadata['anglesx1000']/1e3

    @property
    def monitor(self):
        return self._metadata['monitor']/1e6

    @classmethod
    def from_measurement_string(cls, segment_string):
        metadata = get_metadata(cls.SEGMENT_HEADER_SEPARATOR, segment_string)       
        shot = Shot(metadata)
        shot_counts = get_counts(cls.SEGMENT_HEADER_SEPARATOR, shot.rightmost_angle, segment_string)
        for number, counts in enumerate(shot_counts):
            #counts en realidad viene y es pixel_and_detector_amount esto se arrastra
            shot.add_detector_measurement(number, counts)
        return shot

    def __init__(self, metadata):
        self._metadata = metadata
        self.set_detector_calibration(DEFAULT_CALIBRATION)
        self._detectors = []

    def add_detector_measurement(self, detector_number, counts):
        angle = self.get_detector_angle(detector_number)
        self._detectors.append(Detector(detector_number, self.monitor, angle, counts))

    def get_detector_measurments(self):
        return self._detectors

    def set_detector_calibration(self, detector_angle_calibration):
        '''
        :param detector_angle_calibration: Angular distance from the rightmost detector to every detector.
             The list should have 128 values, with the last value being 0.
        '''
        self._detector_angle_calibration = detector_angle_calibration

    def get_detector_angle(self, detector_number):
        return self.rightmost_angle + self._detector_angle_calibration[-detector_number-1]



class MeasurementsReader:

    SEPARATOR_STRING = 'S'*80
    SEGMENTS_TO_SKIP = 1

    def __init__(self):
        self._shots = []

    def get_measurments_segments(self, file_data):
        return file_data.split(self.SEPARATOR_STRING)[self.SEGMENTS_TO_SKIP:]

    def read_file(self, file_name):
        '''
        Open the file_name and then with (1.1) get_measurments_segments(file_data) obtein segments 
        With each segment 
        '''
        with open(file_name, 'r') as infile:
            file_data = infile.read()
        shot_file_segments = self.get_measurments_segments(file_data)
        for shot_segment in shot_file_segments:
            self._shots.append(Shot.from_measurement_string(shot_segment))

    def get_shots(self):
        return self._shots


def integration_test():
    '''
    This is a test of the integration of the diferent function in this document
    Start using the Class MeasurementsReader() as mr and then call the method read_file (1) 
    and returns shots
    Then (2) for any shots we will show the return from the Class Shot and the 
    method: get_detector_measurments() the detector_number, self.monitor, angle, counts(que no son las cuentas realmente)
    
    '''
    mr = MeasurementsReader()
    mr.read_file('../tests/data/sample_input.txt')
    print ('Found {} shots in the file'.format(len(shots)))
    '''
    for shot_number, shot in enumerate(shots):
        print ('- Shot number: {}'.format(shot_number))
        for detector in shot.get_detector_measurments():
            print ('* {}'.format(detector))
    '''
    return mr.get_shots()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+', help="List of files to import.")
    parser.add_argument("-o", "--output", help="Output file.")
    args = parser.parse_args()


    full_paths = [os.path.join(os.getcwd(), file_path) for file_path in args.files]

    reader = MeasurementsReader()

    for input_file in full_paths:
        reader.read_file(input_file)
    
    with open(args.output, 'wb') as output:
        output.write(pickle.dumps(reader.get_shots()))
