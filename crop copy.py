import subprocess

class VideoProcessor:
    def __init__(self, input_path, x, y, width, height, output):
        self.input_path = input_path
        self.final_output_path = output
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def crop_video(self):
        crop_command = [
            'ffmpeg', '-y', '-i', self.input_path, 
            '-vf', f'crop={self.width}:{self.height}:{self.x}:{self.y}', 
            '-c:v', 'libx264', '-preset', 'fast',  # Example: Using libx264 with fast preset
            '-c:a', 'copy', '-threads', '0',  # Utilize all available threads
            self.final_output_path
        ]
        subprocess.run(crop_command, check=True)

# Example usage
# if __name__ == "__main__":
#     input_video_path = 'input.mp4'
#     x = 178
#     y = 408
#     width = 722
#     height = 1281
#     output_video_path = 'output.mp4'

#     processor = VideoProcessor(input_video_path, x, y, width, height, output_video_path)
#     processor.crop_video()
