import cv2
import numpy as np
from PIL import Image


def main():
    img_path = "/home/pi/piper/image.jpg"
    img = cv2.imread(img_path)
    # Rotate 180
    preprocessed_img = cv2.rotate(img, cv2.ROTATE_180)
    # Get Image Size
    height, width, _ = preprocessed_img.shape[:3]
    print("height : " + str(height))
    print("width : " + str(width))
    # Snipping Image
    preprocessed_img = preprocessed_img[height//7:height//2, 0:width]
    # Convert to Gray
    preprocessed_img = cv2.cvtColor(np.array(preprocessed_img),cv2.COLOR_BGR2GRAY)
    # Do Binary
    ret, preprocessed_img = cv2.threshold(preprocessed_img,100,255,cv2.THRESH_BINARY)
    # Median Blur to remove noise in the image
    # preprocessed_img = cv2.medianBlur(preprocessed_img,3)
    # Save Preprocessed image
    cv2.imwrite("/home/pi/piper/threshold_image.jpg", preprocessed_img)

if __name__ == '__main__':
	main()
