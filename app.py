from main_csv import process_videos_in_folder, Edit_Final_video
from input_video import input_video
import os
import time



file_path = 'temp\\results.csv'
temp_folder = 'crop_video'
output_video_path = 'edited_video'

#save excel File
process_videos_in_folder('ex', temp_folder, file_path)

finalask = input("Can i procced Final rendering [y, n]: ")


if(finalask=='y'):
    #edit final video
    for file_name in os.listdir(temp_folder):
        # Check if the file is a video file (you can add more extensions if needed)
        if file_name.endswith(".mp4"):
            input_video_path = os.path.join(temp_folder, file_name)
            ratio = input_video(input_video_path, edit=True)
    Edit_Final_video(file_path, temp_folder, output_video_path)
else:
    print("Final video Not rendered")

