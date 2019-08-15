import sys

sys.path.append("/opt/ros/kinetic/lib/python2.7/dist-packages")
sys.path.append("/home/sensetime/code/repo_pro/senseauto/build/devel/lib/python2.7/dist-packages")

import cv2

input_image = cv2.imread(sys.argv[1])
input_image[:200, :470, :] = 0

height, width, channel = input_image.shape

input_image[(height - 200):, (width - 200):, :] = 0

input_image = cv2.copyMakeBorder(input_image, 120, 50, 0, 0, cv2.BORDER_CONSTANT)

cv2.imwrite(sys.argv[2], input_image)
