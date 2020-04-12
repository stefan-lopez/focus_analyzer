import numpy as np
import cv2

class VideoHandler():
    def __init__(self, config):
        self.config = config
        self.codec = cv2.VideoWriter_fourcc(*'mpeg')

    # Instantiate the cv2 VideoCapture class and gather relevant screen dimensions
    def capture(self):
        self.video_capture = cv2.VideoCapture(self.config['VIDEO_OPEN_PATH'])
        self.captured_video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.captured_video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.captured_screen_dims = (self.captured_video_width, self.captured_video_height)
        self.create_matrix_indices()
        
        return self
    
    # Instantiate the cv2 VideoWriter class  
    def writer(self):
        self.video_writer = cv2.VideoWriter(self.config['VIDEO_SAVE_PATH'], self.codec, self.config['FPS'], self.captured_screen_dims, True)  
        
        return self
    
    # Create lists of indices for matrix calculations
    def create_matrix_indices(self):
        x_positions = [x for x in range(0, self.captured_screen_dims[0])]
        y_positions = [y for y in range(0, self.captured_screen_dims[1])]  
        self.matrix_indices = [x_positions, y_positions]
    
    # Release the specified class instances from memory
    def release_processes(self, video_capture = True, video_writer = True):
        if video_capture == True:
            self.video_capture.release()
        
        if video_writer == True:
            self.video_writer.release()
        
        return self