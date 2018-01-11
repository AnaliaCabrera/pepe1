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
            
                matrix_per_detector[number,:,base_index] += (np.array(detector.counts)*(1-next_weight))/detector.monitor
                matrix_per_detector[number,:,base_index + 1] += (np.array(detector.counts)*(next_weight))/detector.monitor
        
                matrix_weight_per_detector[number,:,base_index] += [(1-next_weight)]*128
                matrix_weight_per_detector[number,:,base_index + 1] += [(next_weight)]*128
        
        matrix_weighted_per_detector = np.divide(matrix_per_detector, matrix_weight_per_detector,out=np.zeros_like(matrix_per_detector), where = matrix_weight_per_detector != 0 )    
        #muestra donde se superpondrian
        superposted=np.sum(matrix_weighted_per_detector,axis=0)
        
        return matrix_per_detector
    
    def to_matrix(self):
        matrix = np.zeros((self.rows, self.columns))
        matrix_weight = np.zeros((self.rows, self.columns))
        for angle, detectors in self.detectors_per_angle.items():
            
            base_index = int(np.floor((angle-self.min_angle)/self.MATRIX_RESOLUTION))
        
            next_weight = (angle - self.min_angle)/self.MATRIX_RESOLUTION - int(np.floor((angle-self.min_angle)/self.MATRIX_RESOLUTION))
            #print(next_weight)
            for detector in detectors:
                matrix[:,base_index] += (np.array(detector.counts)*(1-next_weight))/detector.monitor
                matrix[:,base_index + 1] += (np.array(detector.counts)*(next_weight))/detector.monitor
              
                matrix_weight[:,base_index] += [(1-next_weight)]*128
                matrix_weight[:,base_index + 1] += [(next_weight)]*128
        
        matrix_weighted = np.divide(matrix, matrix_weight,out=np.zeros_like(matrix), where = matrix_weight != 0 )    
        return matrix_weighted, matrix
    
    
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
    matrix_weighted, matrix = sorter.to_matrix()
    matrix_per_detector = sorter.generate_detector_matrix()

    if args.output is not None:
        with open(args.output, 'wb') as output:
            output.write(pickle.dumps((matrix, matrix_per_detector)))

    if args.plot:
        plt.matshow(matrix_weighted)
        plt.title('matrix_weighted')
        plt.matshow(matrix)
        plt.title('matrix')
        plt.matshow(matrix2)
        plt.title('matrix2')
        plt.show()
