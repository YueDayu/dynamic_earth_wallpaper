import sys
import cv2
import numpy as np

bg_img = cv2.imread('data/bg.jpg')
bg_img = cv2.blur(bg_img,(3, 3))
# avg_img = np.mean(bg_img, axis=2)
# print avg_img.shape
# bg_img[avg_img[:, :] < 200] /= 5
avg_img = np.mean(bg_img, axis=2) / 255.
avg_img = avg_img ** 1.4
h, w, c = bg_img.shape
# for i in range(h):
    # for j in range(w):
        # bg_img = 
bg_img[:, :, 0] = bg_img[:, :, 0] * avg_img
bg_img[:, :, 1] = bg_img[:, :, 1] * avg_img
bg_img[:, :, 2] = bg_img[:, :, 2] * avg_img
cv2.imwrite('data/bg1.jpg', bg_img)
