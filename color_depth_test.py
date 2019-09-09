import os
import cv2
import enum
import numpy as np
from time import sleep

text_file_name = 'color_detection_play.txt'
cap1 = cv2.VideoCapture(1)
cv2.namedWindow('img')

while True:
    _, img = cap1.read()
    img = cv2.flip(img, 1)
    
    roi2 = img
    rgbroi = cv2.cvtColor(roi2, cv2.COLOR_BGR2RGB)
    rgbroi = rgbroi.reshape((-1, 3))
    rgbroi = np.float32(rgbroi)
    
    #K-MEANS
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 2
    ret,label,center = cv2.kmeans(rgbroi,k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((roi2.shape))
    px = center[0]

    text_rgb = ','.join(map(str, px))
    text_rgb += ',0,1,\n'
    print(text_rgb)

    file = open(text_file_name, 'w', encoding = 'utf8')
    file.write(text_rgb)
    file.close()
    
    cv2.imshow('img', img)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap1.release()
