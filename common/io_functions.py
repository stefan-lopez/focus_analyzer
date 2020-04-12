import csv
import moviepy.editor as mpe
import json
import math
import os

# Generate program options from config file
def read_config_options(path):
    with open(path) as config_file:
        config = json.load(config_file)
        
    return config
    
# Gather xy coordinates into a list from eye tracker data
def read_xy_data(path, eye_tracker_screen_dims, video_screen_dims):
    xy_coordinates = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            converted_coordinates = convert_screen_coordinates(row, eye_tracker_screen_dims, video_screen_dims)
            xy_coordinates.append(converted_coordinates)
            
    return xy_coordinates

# Gather eeg signals into a list from eeg data
def read_eeg_data(path):
    eeg_data = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            eeg_data.append(float(row[0]))
        
    return eeg_data

# Combine audio and video files   
def save_combined_av(new_video_path, old_video_path):
    new_videoclip = mpe.VideoFileClip(new_video_path)
    old_videoclip = mpe.VideoFileClip(old_video_path)
    new_videoclip.audio = old_videoclip.audio
    new_videoclip.write_videofile('final_' + new_video_path)
    os.remove(new_video_path)
    
# Convert xy coordinates from one screen size to another    
def convert_screen_coordinates(coordinates, old_screen_dims, new_screen_dims):
    x_ratio = old_screen_dims[0] / new_screen_dims[0]
    y_ratio = old_screen_dims[1] / new_screen_dims[1]
    new_x_coordinate = int(math.floor(float(coordinates[0]) / x_ratio))
    new_y_coordinate = int(math.floor(float(coordinates[1]) / y_ratio))
    
    return [new_x_coordinate, new_y_coordinate]