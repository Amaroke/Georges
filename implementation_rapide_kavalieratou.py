import cv2
import numpy as np

image = cv2.imread("image.png") # Changer le nom
cpt = 0
moyenne = np.average(image)  # MOYENNE/MEDIAN ?
while cpt < 8:
    image = image.astype(int) + moyenne / 10  # /10 ?
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite("processed_image_" + str(cpt) + ".jpg", image)
    cpt += 1
