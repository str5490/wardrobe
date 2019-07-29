import cv2
from enum import Enum
import numpy as np

class Colors_Name(Enum):
    red = 0
    orange = 1
    yellow = 2
    green = 3
    blue = 4
color_num = len(Colors_Name)

colors_rgb = np.zeros([color_num, 3], dtype = int)
colors_rgb[Colors_Name.red.value] = [255, 0, 0]
colors_rgb[Colors_Name.orange.value] = [255, 165, 0]
colors_rgb[Colors_Name.yellow.value] = [255, 255, 0]
colors_rgb[Colors_Name.green.value] = [0, 255, 0]
colors_rgb[Colors_Name.blue.value] = [0, 0, 255]

color_raw = [128, 200, 0]
color_diff = np.zeros([color_num], dtype = int)

for i in Colors_Name:
    color_diff[i.value] = abs(color_raw[0] - colors_rgb[i.value][0])
    color_diff[i.value] += abs(color_raw[1] - colors_rgb[i.value][1])
    color_diff[i.value] += abs(color_raw[2] - colors_rgb[i.value][2])
print (color_diff, color_diff.argmin())
color = color_diff.argmin()

print(Colors_Name(color).name+'.mp3')
print(colors_rgb[color])