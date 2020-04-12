import math
import cv2
import numpy as np

class Transformer():
    def __init__(self, config, eeg_data, eye_tracking_data, matrix_indices):
        self.config = config
        self.eeg_data = eeg_data
        self.eeg_max_val = max(self.eeg_data)
        self.eye_tracking_data = eye_tracking_data
        self.matrix_indices = matrix_indices
        self.aura_colors = self.create_aura_colors()        
    
    # Create list of aura colors for each value in eeg data
    def create_aura_colors(self):
        aura_colors = []
        for val in self.eeg_data:
            color = self.convert_to_rgb(val)
            aura_colors.append(color)
            
        return aura_colors
    
    # Transform a frame into the desired representation of focus and eeg analysis
    def transform_frame(self, frame):
        self.curr_frame = frame
        self.curr_rgb_channels = cv2.split(frame)[::-1]        
        self.curr_xy_pair = self.eye_tracking_data.pop(0) 
        self.curr_aura_color = self.aura_colors.pop(0)        
        self.curr_transformed_frame = self.transform_channels()
        
        return self
                    
    # Convert float values within a range into colors
    def convert_to_rgb(self, value):
        min = self.eeg_max_val * -1
        max = self.eeg_max_val
        halfmax = (min + max) / 2
        if min <= value <= halfmax:
            r = 0
            g = int( 255 / (halfmax - min) * (value - min)) / self.config['HEAT_SENSITIVITY']
            b = int( 255 + (-255 / (halfmax - min)  * (value - min)))  
        else:
            r = int( 255 / (max - halfmax) * (value - halfmax))
            g = int( 255 + (-255 / (max - halfmax)  * (value - halfmax))) / self.config['HEAT_SENSITIVITY']
            b = 0
        
        return (r, g, b)
        
    # Setup matrices that will define the dimensions of the aura circle, focus circle, and background
    def create_matrix_masks(self):
        x_distances = [abs(self.curr_xy_pair[0] - x)**2 for x in self.matrix_indices[0]]
        y_distances = [abs(self.curr_xy_pair[1] - y)**2 for y in self.matrix_indices[1]]

        distances_matrix = [[math.sqrt(x + y) for x in x_distances] for y in y_distances]
        aura_matrix = [[0 if x <= self.config['AURA_RADIUS'] else 1 for x in y] for y in distances_matrix]
        focus_matrix = [[1 if x <= self.config['FOCUS_RADIUS'] else 0 for x in y] for y in distances_matrix]
        neg_focus_matrix = [[0 if x <= self.config['FOCUS_RADIUS'] else 1 for x in y] for y in distances_matrix]
        
        return {'aura' : aura_matrix, 'focus' : focus_matrix, 'neg_focus' : neg_focus_matrix}

    # For each channel, combine matrices with frame's color channel to form a center of focus, aura surrounding the focus, and fuzzy background    
    def apply_masks(self):
        processed_channels = []
        for index, channel in enumerate(self.curr_rgb_channels):
            aura = [[self.curr_aura_color[index] if x == 0 else 0 for x in y] for y in self.curr_matrix_masks['aura']]        
            background = self.curr_matrix_masks['aura'] * channel
            combined_matrix = background + aura
            kernel_matrix = np.ones((20,20), np.float32) / 400
            fuzzy_background = cv2.filter2D(combined_matrix, -1, kernel_matrix)
            focus = self.curr_matrix_masks['focus'] * channel
            final_matrix = focus + (fuzzy_background * self.curr_matrix_masks['neg_focus']) 
            processed_channels.append(final_matrix) 
        
        return processed_channels

    # Transform rgb value channels through the application of matrix masks    
    def transform_channels(self):
        self.curr_matrix_masks = self.create_matrix_masks()        
        self.processed_channels = self.apply_masks()
        self.stacked_channels = np.dstack(self.processed_channels[::-1])
        
        return np.uint8(self.stacked_channels)