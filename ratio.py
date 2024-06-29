import cv2

def get_video_recommendation(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError("Error opening video file")

    # Get the width and height of the video
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    # Release the video capture object
    video.release()
    
    # Find the greatest common divisor (gcd) to simplify the ratio
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    # Calculate the gcd of width and height
    common_divisor = gcd(int(width), int(height))
    
    # Calculate the ratio
    width_ratio = int(width // common_divisor)
    height_ratio = int(height // common_divisor)
    
    # Define standard aspect ratios
    standard_ratios = {
        (1, 1): "Square",
        (9, 16): "Vertical (9:16)",
        (16, 9): "Horizontal (16:9)",
        (2, 1): "Cinematic (2:1)",
        (3, 2): "Classic (3:2)",
        (2, 3): "Vertical (2:3)",
        (1, 2): "Vertical (1:2)"
    }
    
    # Function to check if the calculated ratio is close to a standard ratio within tolerance
    def is_close_to_standard_ratio(width_ratio, height_ratio, tolerance=0.05):
        for (w, h), ratio_name in standard_ratios.items():
            if abs(width_ratio / height_ratio - w / h) < tolerance or abs(height_ratio / width_ratio - h / w) < tolerance:
                return (w, h), ratio_name
        return None, None
    
    # Determine the type of ratio
    ratio_type = is_close_to_standard_ratio(width_ratio, height_ratio)
    
    if ratio_type is None:
        return None
    
    return ratio_type[0]

# Example usage:
# video_path = 'temp_cropped_video.mp4'
# print(get_video_recommendation(video_path))
