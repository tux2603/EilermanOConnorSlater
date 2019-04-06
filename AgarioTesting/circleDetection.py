# -*- coding: utf-8 -*-
# =============================================================================
# Title:
# Author: Ryan J. Slater
# Date: Wed Apr  3 11:31:39 2019
# =============================================================================


# import cv2
# import numpy as np

# img = cv2.imread('Pictures/Screenshots/Screenshot-20190403112444-1270x663.png',0)
# img = cv2.medianBlur(img,5)
# cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
#                             param1=50,param2=30,minRadius=0,maxRadius=0)

# circles = np.uint16(np.around(circles))
# for i in circles[0,:]:
#     # draw the outer circle
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

# cv2.imshow('detected circles',cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread(
    'Pictures/Screenshots/Screenshot-20190403112444-1270x663.png', 0)


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_red = np.array([30, 150, 50])
upper_red = np.array([255, 255, 180])

mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('Original', img)
edges = cv2.Canny(img, 100, 200)
cv2.imshow('Edges', edges)


# edges = cv2.Canny(img, 100, 200)

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

# plt.show()
