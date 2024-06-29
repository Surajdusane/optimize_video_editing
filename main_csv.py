import os
import csv
import re
from snapshot import capture_snapshot
from posize import ImageDetector
from crop import VideoProcessor
from folder_to_file_path import get_files_with_extension
from ocr import detect_text_in_image
from textpng import FinalImageCreator
from whitebgtext import crop_text_from_upper_half
from video_edit_ffmpeg import FinalVideoCreator


def clean_text(text):
    text_no_newlines = text.replace('\n', ' ').replace('\r', ' ').replace('"','')
    clean_text = re.sub(' +', ' ', text_no_newlines)
    return clean_text.strip()

def final_crop_video(input_video, output_path):
    """
    Process a video to capture a snapshot, detect the main image, crop the video, and return the detected text.

    :param input_video: Path to the input video file.
    :param output_path: Path to save the cropped video file.
    :return: Detected text from the snapshot.
    """
    # Step 1: Capture a snapshot from the video
    snapshot_path = 'temp/snapshot.png'
    capture_snapshot(video_path=input_video, output_path=snapshot_path)
    print("Screenshot captured.")

    # Step 2: Detect position and size of the main image in the snapshot
    detector = ImageDetector(snapshot_path, min_width=100, min_height=100)
    detector.process_image()
    x, y, w, h = detector.detect_main_image()
    print("Position defined.")

    # Step 3: Perform OCR on the snapshot to detect text
    crop_text_from_upper_half(snapshot_path, 'temp/ocrtext.png')
    detected_text = detect_text_in_image('temp/ocrtext.png')
    detected_text = clean_text(detected_text)
    print("Text detected:", detected_text)

    # Step 4: Crop the video based on the detected position and size
    processor = VideoProcessor(input_video, x, y, w, h, output=output_path)
    processor.crop_video()
    print("Video processed successfully.")

    return detected_text

def process_videos_in_folder(input_folder, output_folder, csv_output_path):
    """
    Process all videos in a folder using final_crop_video and save results to a CSV file.

    :param input_folder: Path to the folder containing input videos.
    :param output_folder: Path to the folder to save processed videos.
    :param csv_output_path: Path to save the CSV file with video paths and detected text.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_files = get_files_with_extension(input_folder, 'mp4')
    results = []

    for idx, video_file in enumerate(video_files):
        video_name = os.path.basename(video_file)
        output_video_path = os.path.join(output_folder, f"{idx}.mp4")
        detected_text = final_crop_video(video_file, output_video_path)
        results.append([video_file, detected_text])
        print(f"Processed {video_file}")

    with open(csv_output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Video Path", "Detected Text"])
        writer.writerows(results)

    print(f"Results saved to {csv_output_path}")


def Edit_Final_video(csv_file_path,input_path,output_path):
    # Create an empty dictionary to hold the data
    data = {}

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Extract the header (column titles)
        header = next(csv_reader)
        
        # Initialize the dictionary with the column titles as keys and empty lists as values
        for column in header:
            data[column] = []
        
        # Iterate through the remaining rows
        for row in csv_reader:
            for i, value in enumerate(row):
                data[header[i]].append(value)
    
    # Iterate through the data
    for i in range(len(data['Video Path'])):
        text_image = FinalImageCreator()
        text_image.create_final_image(data['Detected Text'][i], "temp/outputtext.png")
        print("Text image created.")

        # Step 8: Create the final edited video with overlaid text image
        creator = FinalVideoCreator(f'{input_path}/{i}.mp4', "temp/outputtext.png", "assets/grain.png", f'{output_path}//{i}.mp4', carousels=True,audio=True,audio_path='assets\\audi.mp3',fadein=False)
        creator.create_final_video()
        print(f"Final video created: {input_path}/{output_path}{i}.mp4")

print("All videos processed successfully.")