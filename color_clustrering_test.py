
import numpy as np
import cv2

image = cv2.imread('clustering_test.jpg')
temp = image.reshape((-1, 3))

temp = np.float32(temp)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0)
K = 2
attemps = 10
ret, label, center = cv2.kmeans(temp, K, None, criteria, attemps, cv2.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
print('ret:', ret)
print('label:', label)
print('center:', center)

num_label = np.zeros(K, dtype = int)
for i in label:
    num_label[i] += 1
major_color_index = num_label.argmax()
one_pixel = np.uint8([[center[major_color_index]]])
major_color = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2RGB)
print('major_color:', major_color)

res = center[label.flatten()]
res2 = res.reshape((image.shape))
cv2.imshow('res2', res2)
cv2.waitKey(0)
cv2.destroyAllWindows()
