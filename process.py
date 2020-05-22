import sys
import cv2
import numpy as np
import json

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

input_image = cv2.copyMakeBorder(input_image, 200, 150, 0, 0, cv2.BORDER_CONSTANT)


def get_valid_range(img, axis):
    x_sum = np.mean(img, axis=axis)
    a_sum = np.min(x_sum, axis=1)
    z_idx = np.where(a_sum > 1)[0]
    return z_idx[0], z_idx[-1]


def get_center_r(h_range, w_range):
    h_c = float(h_range[0] + h_range[1]) / 2.
    w_c = float(w_range[0] + w_range[1]) / 2.
    r = (float(h_range[1] - h_range[0]) / 2. + float(w_range[1] - w_range[0]) / 2.) / 2.
    return (h_c, w_c), r


def save_config(n_h, n_w, center, r):
    outfile = open("earth_config.json", 'w')
    dump_data = {
        'h': n_h,
        'w': n_w,
        'center_h': center[0],
        'center_w': center[1],
        'r': r
    }
    json.dump(dump_data, outfile)
    outfile.close()


def load_config():
    try:
        infile = open('earth_config.json')
        data = json.load(infile)
        return True, data['h'], data['w'], (data['center_h'], data['center_w']), data['r']
    except Exception as e:
        return False, 0, 0, (0, 0), 0


if len(sys.argv) > 2:
    bg_image = cv2.imread(sys.argv[3])
    i_h, i_w, i_c = input_image.shape
    b_h, b_w, b_c = bg_image.shape
    n_h = min(b_h, i_h)
    n_w = int(float(n_h) / i_h * i_w)
    new_input_image = cv2.resize(input_image, (n_w, n_h), interpolation=cv2.INTER_NEAREST)
    res, h, w, center_pt, r = load_config()
    if (not res) or h != n_h or w != n_w:
        h_range = get_valid_range(new_input_image, 1)
        w_range = get_valid_range(new_input_image, 0)
        center_pt, r = get_center_r(h_range, w_range)
        save_config(n_h, n_w, center_pt, r)
        mask_img = np.zeros((n_h, n_w), dtype=np.uint8)
        for i in range(n_h):
            for j in range(n_w):
                if (float(i) - center_pt[0]) ** 2 + (float(j) - center_pt[1]) ** 2 < r ** 2:
                    mask_img[i, j] = 255
        cv2.imwrite("mask.png", mask_img)

    mask_img = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)

    start_x = int((b_w - n_w) / 2)
    start_y = int((b_h - n_h) / 2)
    center_img = bg_image[start_y:start_y+n_h, start_x:start_x+n_w, :]
    center_img[mask_img[:, :] > 0] = new_input_image[mask_img[:, :] > 0]
    input_image = bg_image
    input_image[start_y:start_y+n_h, start_x:start_x+n_w, :] = center_img

cv2.imwrite(sys.argv[2], input_image)
