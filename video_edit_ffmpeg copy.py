import ffmpeg
import json
from ratio import get_video_recommendation
from delete import delete_file

class FinalVideoCreator:
    def __init__(self, overlay_video_path, overlay_image_path, grain, output_video_path, delete=False, audio=False, audio_path=None, carousels=False, fadein=True):
        self.overlay_video_path = overlay_video_path
        self.overlay_image_path = overlay_image_path
        self.grain = grain
        self.output_video_path = output_video_path
        self.delete = delete
        self.audio = audio
        self.audio_path = audio_path
        self.carousels = carousels
        self.fadein = fadein

    def video_size(self):
        video_ratio = get_video_recommendation(self.overlay_video_path)
        ratio_map = {
            (1, 1): "1:1",
            (2, 1): "2:1",
            (1, 2): "1:2",
            (9, 16): "9:16",
            (16, 9): "16:9",
            (2, 3): "2:3",
            (3, 2): "3:2",
            None: "9:16"
        }
        ratio_vid_key = ratio_map.get(video_ratio, None)
        if ratio_vid_key is None:
            raise ValueError("Unsupported video ratio")
        print(ratio_vid_key)

        if self.carousels:
            with open("assets/video_pns_carousels.json", 'r') as file:
                ratio_data = json.load(file)
                ratio_vid = ratio_data[ratio_vid_key]
        else:
            with open("assets/video_pns_reels.json", 'r') as file:
                ratio_data = json.load(file)
                ratio_vid = ratio_data[ratio_vid_key]

        self.main_height = ratio_vid["height"]
        self.main_width = ratio_vid["width"]
        self.main_top = ratio_vid["top"]
        self.main_left = ratio_vid["left"]

    def get_video_duration(self, video_path):
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream and 'duration' in video_stream:
            return float(video_stream['duration'])
        else:
            raise ValueError("Could not determine video duration")

    def create_final_video(self):
        # Initialize video size attributes
        self.video_size()

        # Convert centimeters to pixels
        def Cm(value):
            return value * 37.7953

        # Set the position and size for the overlay video
        left = Cm(self.main_left)
        top = Cm(self.main_top)
        overlay_width = Cm(self.main_width)
        overlay_height = Cm(self.main_height)

        # Set the resolution for the white screen
        if self.carousels:
            width, height = 1080, 1350
        else:
            width, height = 1080, 1920

        # Get the duration of the overlay video
        duration = self.get_video_duration(self.overlay_video_path)

        # Construct the FFmpeg filtergraph
        input_video = ffmpeg.input(self.overlay_video_path)
        input_image = ffmpeg.input(self.overlay_image_path)
        input_grain = ffmpeg.input(self.grain)

        # Apply filters to the video
        if(self.fadein):
            video = (
                input_video
                .filter('hflip')  # Horizontal flip
                .filter('fade', type='in', start_time=0, duration=1)
                .filter('eq', brightness=0.03)
                .filter('eq', contrast=1.1)
                .filter('scale', overlay_width, overlay_height)
            )
        else:
            video = (
                input_video
                .filter('hflip')  # Horizontal flip
                .filter('eq', brightness=0.03)
                .filter('eq', contrast=1.1)
                .filter('scale', overlay_width, overlay_height)
            )

        # Create a white background
        white_background = (
            ffmpeg.input('color=white:s={}x{}:d={}'.format(width, height, duration), f='lavfi')
        )
        cm_to_pixels = 37.7952756
        if self.carousels:
            height_pixels = 5.72 * cm_to_pixels
            width_pixels = 18.6 * cm_to_pixels
            top_pixels = 0.93 * cm_to_pixels
            left_pixels = 4.99 * cm_to_pixels
        else:
            height_pixels = 5.72 * cm_to_pixels
            width_pixels = 17.55 * cm_to_pixels
            top_pixels = 4.07 * cm_to_pixels
            left_pixels = 5.72 * cm_to_pixels

        # Prepare the overlay image
        overlay_image = (
            input_image
            .filter('scale', width_pixels, height_pixels)
        )

        # Prepare the grain overlay
        overlay_grain = (
            input_grain
            .filter('scale', overlay_width, overlay_height)
        )

        # Overlay video on white background
        combined = (
            white_background.overlay(video, x=left, y=top)
            .overlay(overlay_image, x=left_pixels, y=top_pixels)
            .overlay(overlay_grain, x=left, y=top)
        )

        # Output file setup
        if self.audio and self.audio_path:
            input_audio = ffmpeg.input(self.audio_path)
            final_output = ffmpeg.output(combined, input_audio, self.output_video_path, vcodec='libx264', acodec='aac', audio_bitrate='192k', shortest=None)
        else:
            final_output = combined.output(self.output_video_path, vcodec='libx264', acodec='aac')

        # Run FFmpeg command
        final_output = final_output.overwrite_output().run()

        # Deleting input video if specified
        if self.delete:
            delete_file(self.overlay_video_path)
            print(f"{self.overlay_video_path} Video is deleted!!")


# Example usage:
# if __name__ == "__main__":
#     creator = FinalVideoCreator(
#         overlay_video_path="r\\0.mp4",
#         overlay_image_path="temp\\outputtext.png",
#         grain="assets\\grain.png",
#         output_video_path="edit\\output_video.mp4",
#         delete=False,
#         audio=True,
#         audio_path="assets\\audi.mp3",
#         carousels=False
#     )
#     creator.create_final_video()
