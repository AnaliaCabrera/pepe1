# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 04:36:56 2018

@author: Ana Cabrera
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pickle

class DetectorSorter:
    MATRIX_RESOLUTION = 0.05

    def __init__(self, shot_list):
        self._shot_list = shot_list
        self.detectors_per_angle = self.order_per_angle()
        self.detectors_per_number = self.order_per_detector_number()
        angles = self.detectors_per_angle.keys()
        self.min_angle = min(angles)
        self.max_angle = max(angles)

        self.columns = int((self.max_angle - self.min_angle) / self.MATRIX_RESOLUTION )+3
        self.rows = 128

    def detector_iterator(self):
        for shot in self._shot_list:
            for detector in shot.get_detector_measurments():
                yield detector

    def order_per_angle(self):
        detectors_per_angle = {}
        for detector in self.detector_iterator():
            if detector.angle in detectors_per_angle:
                detectors_per_angle[detector.angle].append(detector)
            else:
                detectors_per_angle[detector.angle] = [detector]

        #print(detectors_per_angle)
        return detectors_per_angle

    def order_per_detector_number(self):
        detectors_per_number = {}
        for detector in self.detector_iterator():
            if detector.number in detectors_per_number:
                detectors_per_number[detector.number].append(detector)
            else:
                detectors_per_number[detector.number] = [detector]

        return detectors_per_number

    def generate_detector_matrix(self):
        #nuevo
        matrix_per_detector=np.zeros((self.rows, self.rows, self.columns))
        matrix_weight_per_detector=np.zeros((self.rows, self.rows, self.columns))
        for number, detectors in self.detectors_per_number.items():
            for detector in detectors:
                angle=detector.angle
                base_index = int(np.floor((angle-self.min_angle)/self.MATRIX_RESOLUTION))
                next_weight = (angle-self.min_angle)/self.MATRIX_RESOLUTION - int(np.floor((angle-self.min_angle)/self.MATRIX_RESOLUTION))
                # '1': correlate with comment '2' in fole measurement_reader.py
                detector.counts.reverse()
                matrix_per_detector[number,:,base_index] += (np.array(detector.counts)*(1-next_weight))/detector.monitor
                matrix_per_detector[number,:,base_index + 1] += (np.array(detector.counts)*(next_weight))/detector.monitor

                matrix_weight_per_detector[number,:,base_index] += [(1-next_weight)]*128
                matrix_weight_per_detector[number,:,base_index + 1] += [(next_weight)]*128

        matrix_weighted_per_detector = np.divide(matrix_per_detector, matrix_weight_per_detector,out=np.zeros_like(matrix_per_detector), where = matrix_weight_per_detector != 0 )
        #muestra donde se superpondrian
        superposted=np.sum(matrix_weighted_per_detector,axis=0)

        return matrix_per_detector

    def to_matrix(self):
        angles = []
        for detector in self.detector_iterator():
            angles.append(detector.angle)
        min_angle = min(angles)
        max_angle = max(angles)
        columns = int((max_angle-min_angle)/self.MATRIX_RESOLUTION)+3
        matrix_total = np.zeros((128, columns))
        matrix_weights = np.zeros((128, columns))
        matrix_not_split = np.zeros((128, columns))

        for detector in self.detector_iterator():
            base_index = int(np.floor((detector.angle-min_angle)/self.MATRIX_RESOLUTION))
            next_weight = (detector.angle - min_angle)/self.MATRIX_RESOLUTION - int(np.floor((detector.angle-min_angle)/self.MATRIX_RESOLUTION))
            # Only leave the following line of we are saving the lowest pixel on the position 0.
            # '1': correlate with comment '2' in fole measurement_reader.py
            detector.counts.reverse()
            matrix_total[:, base_index] += (np.array(detector.counts)*(1-next_weight)) /detector.monitor
            matrix_total[:, base_index+1] += (np.array(detector.counts)*(next_weight)) /detector.monitor

            matrix_weights[:,base_index] += np.array([1-next_weight]*128)
            matrix_weights[:,base_index+1] += np.array([next_weight]*128)

            matrix_not_split[:, base_index] += np.array(detector.counts)

        matrix_weighted = np.divide(matrix_total, matrix_weights, out=np.zeros_like(matrix_total), where=matrix_weights != 0 )

        return matrix_weighted, matrix_total, matrix_not_split

if __name__ == '__main__':
    from d2b_tools.measurements_reader import Detector, Shot
    parser = argparse.ArgumentParser()
    parser.add_argument("shots_file", help="Pickled shots file to import.")
    parser.add_argument("-o", "--output", help="Output file.")
    parser.add_argument("-p", "--plot", action="store_true", help="Plot matrix and weighted matrix.")
    args = parser.parse_args()

    with open(args.shots_file, 'rb') as input_file:
        shots = pickle.load(input_file)

    sorter = DetectorSorter(shots)
    # sorter.to_matrix_no_dict()
    matrix_per_detector = sorter.generate_detector_matrix()
    matrix_weighted, matrix_total, matrix_not_split = sorter.to_matrix()

    if args.output is not None:
        with open(args.output, 'wb') as output:
            output.write(pickle.dumps((matrix_weighted, matrix_total, matrix_per_detector)))

    if args.plot:
        plt.matshow(matrix_weighted)
        plt.title('matrix_weighted')
        plt.matshow(matrix_total)
        plt.title('matrix_total')
        plt.matshow(matrix_not_split)
        plt.title('matrix_not_split')
        plt.show()
