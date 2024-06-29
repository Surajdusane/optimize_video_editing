import cv2
from PIL import Image
import numpy as np

def crop_text_from_upper_half(image_path, output_path=None):
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Image at path '{image_path}' could not be loaded.")
    
    # Get image dimensions
    height, width, _ = image.shape
    
    # Crop to the upper half of the image
    upper_half = image[:height // 2, :]
    
    # Convert the upper half to grayscale
    gray = cv2.cvtColor(upper_half, cv2.COLOR_BGR2GRAY)
    
    # Apply a binary threshold to get a binary image
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize variables to find the bounding box of all text
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = 0, 0
    
    # Loop through each contour to find the overall bounding box
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)
    
    # Ensure we found some text, otherwise set the bounding box to the whole upper half
    if min_x == float('inf') or min_y == float('inf'):
        min_x, min_y, max_x, max_y = 0, 0, width, height // 2
    
    # Crop the image to the bounding box of the text
    cropped_image = upper_half[min_y:max_y, min_x:max_x]
    
    # Convert the cropped image to PIL format
    cropped_image_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    
    # Save or return the cropped image
    if output_path:
        cropped_image_pil.save(output_path)
    else:
        return cropped_image_pil

# Example usage
# crop_text_from_upper_half('ext.png', 't.jpg')
