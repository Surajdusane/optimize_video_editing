import cv2

class ImageDetector:
    def __init__(self, image_path, min_width=100, min_height=100):
        self.image_path = image_path
        self.min_width = min_width
        self.min_height = min_height
        self.image = None
        self.gray_image = None
        self.binary_image = None
        self.contours = None

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError("Image not found or unable to load.")
        return self.image

    def convert_to_grayscale(self):
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return self.gray_image

    def apply_threshold(self):
        _, self.binary_image = cv2.threshold(self.gray_image, 240, 255, cv2.THRESH_BINARY_INV)
        return self.binary_image

    def find_contours(self):
        self.contours, _ = cv2.findContours(self.binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return self.contours

    def detect_main_image(self):
        main_x, main_y, main_w, main_h = 0, 0, 0, 0
        for contour in self.contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > self.min_width and h > self.min_height:
                main_x, main_y, main_w, main_h = x, y, w, h
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #print(f"Position: ({x}, {y}), Width: {w}, Height: {h}")
        return main_x, main_y, main_w, main_h

    def display_image(self):
        cv2.imshow('Detected Objects', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def process_image(self):
        self.load_image()
        self.convert_to_grayscale()
        self.apply_threshold()
        self.find_contours()
        self.detect_main_image()
        #self.display_image()

# Usage
# detector = ImageDetector('snapshot.png', min_width=100, min_height=100)
# detector.process_image()
# x, y, w, h = detector.detect_main_image()
# print(x)