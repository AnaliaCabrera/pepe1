# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 04:36:56 2018

@author: Ana Cabrera
"""
import numpy as np
import matplotlib.pyplot as plt

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
            

        #print(detectors_per_angle)
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
        '''
        plt.figure(10)
        plt.imshow(matrix_weighted_per_detector[18],clim=(0.1,60))
        
        plt.figure(12)
        plt.imshow(matrix_weight_per_detector[18])
        '''
        plt.figure(13)
        plt.imshow(superposted,clim=(0.1,60))
        
        plt.figure(11)
        plt.imshow(matrix_weighted_per_detector[120],clim=(0.1,60))            
        
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
        
        print(matrix_weighted)
        plt.figure(0)
        plt.imshow(matrix_weighted,clim=(0.1,60))
        '''
        plt.figure(1)
        plt.hist(matrix_weighted.ravel(), bins=266, range=(0.01, 40), fc='k', ec='k')
        plt.figure(2)
        plt.hist(matrix_weight.ravel(), bins=266, range=(0.01, 40), fc='k', ec='k')
        plt.figure(3)
        plt.hist(matrix.ravel(), bins=266, range=(0.01, 40), fc='k', ec='k')
        '''
        return matrix_weighted
    
    
    def to_search_efficiency_raw(self):
        matrix_weighted = self.to_matrix()
        matrix_per_detector = self.generate_detector_matrix()
        for a in range(20,60):
            efficency_raw=np.divide(matrix_weighted, matrix_per_detector[a])
        plt.figure(200)
        plt.imshow(efficency_raw,clim=(0.5,1.5))
        plt.figure(200+1)
        plt.hist(efficency_raw.ravel(), bins=266, range=(0.01, 2), fc='k', ec='k')
if __name__ == '__main__':
    from d2b_tools import measurements_reader
    shots = measurements_reader.integration_test()
    ds = DetectorSorter(shots)
    ds.order_per_angle()
    ds.to_matrix()
    ds.generate_detector_matrix()
    ds.to_search_efficiency_raw()