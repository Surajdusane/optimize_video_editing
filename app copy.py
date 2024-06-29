from main_csv import process_videos_in_folder, Edit_Final_video
from input_video import input_video
import os
import time
import csv

file_path = 'temp\\results.csv'
temp_folder = 'crop_video'
output_video_path = 'edited_video'
report_file_path = 'temp\\report.csv'

# Save Excel File
process_videos_in_folder('ex copy', temp_folder, file_path)

#finalask = input("Can I proceed with final rendering [y, n]: ")
finalask = 'y'

if finalask == 'y':
    report_data = []
    
    # Edit final video
    for file_name in os.listdir(temp_folder):
        # Check if the file is a video file (you can add more extensions if needed)
        if file_name.endswith(".mp4"):
            input_video_path = os.path.join(temp_folder, file_name)
            
            start_time = time.time()
            ratio = input_video(input_video_path, edit=True)
            end_time = time.time()
            
            processing_time = end_time - start_time
            fps = ratio  # Assuming the 'ratio' returned by input_video is the FPS
            
            # Collect data for the report
            report_data.append({
                'video_name': file_name,
                'processing_time': processing_time,
                'fps': fps
            })
    
    Edit_Final_video(file_path, temp_folder, output_video_path)
    
    # Write report data to CSV file
    with open(report_file_path, mode='w', newline='') as report_file:
        fieldnames = ['video_name', 'processing_time', 'fps']
        writer = csv.DictWriter(report_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in report_data:
            writer.writerow(data)
    
    print(f"Report generated: {report_file_path}")
else:
    print("Final video not rendered")
