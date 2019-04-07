import cv2
import numpy as np
from time import time
import os

os.system('clear')

img = cv2.imread('Screenshots/screenshot_600x400_2019-04-06 20-04-38.png', 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=20, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))

for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)


# =============== RYANS CODE ===================

circles = circles[0]
usIndex = 0
minDistance = 10000000
for i in range(len(circles)):
    print(circles[i][2])
    if circles[i][2] > 6:
        if abs(circles[i][0] - 2 * circles[i][1]) < minDistance:
            minDistance = abs(circles[i][0] - 2 * circles[i][1])
            usIndex = i

print('Us: {}'.format(circles[i]))
cv2.circle(cimg, (circles[i][0], circles[i][1]), circles[i][2], (255, 0, 0), 2)

# ================================================

cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()