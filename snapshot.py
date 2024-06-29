import cv2

def capture_snapshot(video_path, output_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    # Get the frame rate (frames per second)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # Calculate the frame number for 2 seconds
    frame_number = int(fps * 2)

    # Set the video position to the frame number
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame at the specified position
    success, frame = video.read()

    # If reading the frame was not successful, exit
    if not success:
        print("Error: Could not read frame.")
        return

    # Save the frame as a PNG image
    cv2.imwrite(output_path, frame)

    # Release the video object and close the window
    video.release()
    cv2.destroyAllWindows()

# Example usage:
# video_file = 'ex.mp4'  # Replace with your video file path
# output_file = 'snapshot.png'  # Output file path for the snapshot

# capture_snapshot(video_file, output_file)
