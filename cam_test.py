import cv2
import numpy as np

def setup_change(x):
    brightness = cv2.getTrackbarPos('brightness', 'setup')
    contrast = cv2.getTrackbarPos('contrast', 'setup')
    saturation = cv2.getTrackbarPos('saturation', 'setup')
    exposure = cv2.getTrackbarPos('exposure', 'setup')
    cap1.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    cap1.set(cv2.CAP_PROP_CONTRAST, contrast)
    cap1.set(cv2.CAP_PROP_SATURATION, saturation)
    cap1.set(cv2.CAP_PROP_EXPOSURE, -exposure)
    pass

cap1 = cv2.VideoCapture(1)

brightness = int(cap1.get(cv2.CAP_PROP_BRIGHTNESS))
contrast = int(cap1.get(cv2.CAP_PROP_CONTRAST))
saturation = int(cap1.get(cv2.CAP_PROP_SATURATION))
exposure = int(cap1.get(cv2.CAP_PROP_EXPOSURE))
print('brightness', brightness)
print('contrast', contrast)
print('saturation', saturation)
print('exposure', exposure)

cv2.namedWindow('setup')

cv2.createTrackbar('brightness','setup',0,10,setup_change)
cv2.createTrackbar('contrast','setup',0,10,setup_change)
cv2.createTrackbar('saturation','setup',0,10,setup_change)
cv2.createTrackbar('exposure','setup',0,100,setup_change)

cv2.setTrackbarPos('brightness','setup',brightness)
cv2.setTrackbarPos('contrast','setup',contrast)
cv2.setTrackbarPos('saturation','setup',saturation)
cv2.setTrackbarPos('exposure','setup',-exposure)

while True: 
    try:
        _, frame = cap1.read()
        frame = cv2.flip(frame, 1)
    except:
        pass
        
    cv2.imshow('frame', frame)
        
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap1.release()
