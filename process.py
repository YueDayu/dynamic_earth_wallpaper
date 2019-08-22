import sys
import cv2
import numpy as np

input_image = cv2.imread(sys.argv[1])
input_image[:200, :470, :] = 0

height, width, channel = input_image.shape

input_image[(height - 200):, (width - 200):, :] = 0

yellow_lower = np.array([26, 60, 45], np.uint8)
yellow_upper = np.array([34, 255, 255], np.uint8)
hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

night_light = np.zeros((height, width, 3), dtype=np.uint8)
night_light[yellow == 255] = np.array([0, 170, 240], dtype=np.uint8)
night_light = cv2.blur(night_light, (5, 5))

weight = night_light[:, :, 2] / 255. / 1.5
night_light[:, :, 0] = night_light[:, :, 0] * weight
night_light[:, :, 1] = night_light[:, :, 1] * weight
night_light[:, :, 2] = night_light[:, :, 2] * weight
input_image[:, :, 0] = input_image[:, :, 0] * (1 - weight)
input_image[:, :, 1] = input_image[:, :, 1] * (1 - weight)
input_image[:, :, 2] = input_image[:, :, 2] * (1 - weight)
input_image = input_image + night_light

input_image = cv2.copyMakeBorder(input_image, 120, 50, 0, 0, cv2.BORDER_CONSTANT)

cv2.imwrite(sys.argv[2], input_image)
