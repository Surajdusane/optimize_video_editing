from PIL import Image, ImageDraw, ImageFont
import textwrap
import json

class TextImageCreator:
    def __init__(self, text, height_px, width_px, wrap=10, font_path="assets\\Poppins-Regular.ttf", font_size=212):
        self.text = text
        self.height_px = height_px
        self.width_px = width_px
        self.wrap = wrap
        self.font_path = font_path
        self.font_size = font_size
        
        self.image = Image.new("RGBA", (self.width_px, self.height_px), (255, 255, 255, 0))
        self.font = ImageFont.truetype(self.font_path, self.font_size)
        self.draw = ImageDraw.Draw(self.image)
    
    def wrap_text(self):
        return textwrap.wrap(self.text, width=self.wrap)
    
    def calculate_line_height(self):
        line_metrics = self.font.getmetrics()
        return line_metrics[0] + line_metrics[1] // 2
    
    def draw_text(self):
        lines = self.wrap_text()
        line_height = self.calculate_line_height()
        total_text_height = len(lines) * line_height
        y_start = (self.height_px - total_text_height) // 2

        for line in lines:
            bbox = self.draw.textbbox((0, 0), line, font=self.font)
            line_width = bbox[2] - bbox[0]
            x = (self.width_px - line_width) // 2
            y = y_start

            self.draw.text((x, y), line, font=self.font, fill="black")
            y_start += line_height

    def create_image(self):
        self.draw_text()
        return self.image

class LengthCalculator:
    @staticmethod
    def calculate(text):
        thresholds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
        tl = len(text)
        
        for threshold in thresholds:
            if tl <= threshold:
                return str(threshold)
        
        return '150'

class FinalImageCreator:
    def __init__(self):
        with open('assets\\textsize.json', "r") as file:
            self.data = json.load(file)
    
    def create_final_image(self, text, output):
        text_length = LengthCalculator.calculate(text)
        wrap = int(self.data[text_length]['wrap'])
        font_size = int(self.data[text_length]['font_size'])
        
        text_image_creator = TextImageCreator(text, 900, 2700, wrap=wrap, font_size=font_size)
        image = text_image_creator.create_image()
        image.save(output)

# Usage
# final_image_creator = FinalImageCreator()
# final_image_creator.create_final_image("Your text here", "tempsnap\\output.png")




