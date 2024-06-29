from ratio import get_video_recommendation
from black_bars import convert_to_1080x1920
from delete import delete_file
import os

def input_video(video, edit=False):
    video_ratio = get_video_recommendation(video)
    ratio_map = {
            (1, 1): "1:1",
            (2, 1): "2:1",
            (1, 2): "1:2",
            (9, 16): "9:16",
            (16, 9): "16:9",
            (2, 3): "2:3",
            (3, 2): "3:2",
        }
    ratio = ratio_map.get(video_ratio, "9:16None")
    if ratio == "9:16None":
        if(edit):
            convert_to_1080x1920(video)
        else:
            delete_file(video)

# print(input_video("ransize video.mp4"))


# for file_name in os.listdir("r"):
#     # Check if the file is a video file (you can add more extensions if needed)
#     if file_name.endswith(".mp4"):
#         input_video_path = os.path.join("r", file_name)
#         ratio = input_video(input_video_path, edit=True)
