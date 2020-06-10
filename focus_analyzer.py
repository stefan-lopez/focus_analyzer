import cv2
from common.io_functions import read_config_options, read_xy_data, read_eeg_data, save_combined_av
from common.transformer import Transformer
from common.video_handler import VideoHandler

# Load program options from config file
config = read_config_options('configs/config.json') 

# Instantiate class to handle video files
VideoHandler = VideoHandler(config).capture().writer()

# Read in eeg and eye tracking data
eeg_data = read_eeg_data(config['EEG_DATA_PATH'])
eye_tracking_data = read_xy_data(config['EYE_TRACKING_DATA_PATH'], config['EYE_TRACKER_SCREEN_DIMS'], VideoHandler.captured_screen_dims)

# Instantiate class to use eeg and eye tracking data to transform videos
Transformer = Transformer(config, eeg_data, eye_tracking_data, VideoHandler.matrix_indices)

# Iterate through each frame of video, apply transformations to rgb values and re-write the results
def main():
    while VideoHandler.video_capture.isOpened():
        frame_present, frame = VideoHandler.video_capture.read()
        
        # Check for eye tracking data, eeg data, and available frames. If present, apply transformations to frame and write the results.
        if frame_present and  min([len(eeg_data), len(eye_tracking_data)]) > 0:
            Transformer.transform_frame(frame)
            VideoHandler.video_writer.write(Transformer.curr_transformed_frame)
            
            # Toggle whether to display video being edited in real time
            if config['HEADLESS'] == False:
                cv2.imshow('frame', Transformer.curr_transformed_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break   
        else:
            break

    # Release all video processes from memory
    VideoHandler.release_processes()
    cv2.destroyAllWindows()

    # Save new video with audio from the original video
    save_combined_av(config['VIDEO_SAVE_PATH'], config['VIDEO_OPEN_PATH'])
    
if __name__ == '__main__':
    main()
