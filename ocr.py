from PIL import Image
import pytesseract

def detect_text_in_image(image_path):
    try:
        try:
            # Open the image file
            img = Image.open(image_path)
            
            # Use pytesseract to do OCR on the image
            text = pytesseract.image_to_string(img)
            
            return text
        except Exception as e:
            return str(e)
    except Exception as e:
        return str("None")


# # Example usage:
# image_path = 'Serene Office Collaboration.jpg'
# detected_text = detect_text_in_image(image_path)
# print(detected_text)