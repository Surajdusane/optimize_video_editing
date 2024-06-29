import subprocess
import os

def fix_moov_atom(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c', 'copy',
        '-map', '0',
        '-movflags', '+faststart',
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Fixed moov atom for: {output_path}")
        return True
    except subprocess.CalledProcessError:
        return False

def convert_to_1080x1920(input_path):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Check if input video can be opened
    try:
        subprocess.run(['ffmpeg', '-v', 'error', '-i', input_path, '-f', 'null', '-'], check=True)
    except subprocess.CalledProcessError:
        print("Error opening video file. Attempting to fix moov atom...")
        fixed_path = input_path + "_fixed.mp4"
        if not fix_moov_atom(input_path, fixed_path):
            raise ValueError("Error opening video file. The video file might be corrupted or not in the correct format.")
        input_path = fixed_path

    temp_output_path = input_path + "_temp.mp4"

    command = [
        'ffmpeg', 
        '-i', input_path,
        '-vf', 'scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '22',
        temp_output_path,
        '-y'  # This flag overwrites the output file without asking
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video conversion successful: {temp_output_path}")
        os.replace(temp_output_path, input_path)  # Rename temp file to original file
        print(f"Replaced original file with converted video: {input_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

# Example usage
# input_video_path = "saved_files\\2020-12-15_08-10-48_UTC.mp4"
# convert_to_1080x1920(input_video_path)
