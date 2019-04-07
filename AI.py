from math import sin, cos, pi, atan2, sqrt
from PIL import Image, ImageColor
from time import time
import numpy as np
import collections
import colorsys
import cv2
from ArrToVideo import VideoOutput
from numba import jit


class AI:
    def __init__(self, imageCenterX, imageCenterY):
        self.mode = 'defend'
        self.angularRes = 4
        self.radialRes = 10
        self.numRings = 40
        self.firstRing = 35

        self.imageCenterX = imageCenterX
        self.imageCenterY = imageCenterY

        self.radiusHistory = []

        self.targetChange = time() - 100
        self.lastTarget = 0

        self.videoOut = VideoOutput(self.angularRes, self.radialRes, self.firstRing, self.numRings)

    def __attack__(self, image):
        image = image.convert('RGB')
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.medianBlur(image, 5)
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=20, minRadius=0, maxRadius=0)
        circles = np.uint16(np.around(circles))

        # Remove bad circles

        USX = 300
        USY = 240

        circlesCondensed = circles[0]
        usIndex = -1
        maxRadius = 0
        minDistance = 100000000
        for i in range(len(circlesCondensed)):
            if abs(300 - circlesCondensed[i][0]) < 25:
                if abs(150 - circlesCondensed[i][1]) < 25:
                    if circlesCondensed[i][2] > 20:
                        if sqrt((300 - circlesCondensed[i][0]) ** 2 + (150 - circlesCondensed[i][1]) ** 2) < minDistance:
                            minDistance = sqrt((300 - circlesCondensed[i][0]) ** 2 + (150 - circlesCondensed[i][1]) ** 2)
                            usIndex = i

        # Update Radius
        if usIndex != -1:
            self.radiusHistory.append(circlesCondensed[usIndex][2])
            if len(self.radiusHistory) > 15:
                self.radiusHistory.pop(0)
            avgRadius = int(sum(self.radiusHistory) / len(self.radiusHistory) / 2)
            self.firstRing = avgRadius + 15
            print('Radius: {} px'.format(avgRadius))

        # Find highest density of food
        # target = 0
        # for circle in circlesCondensed:
        #     if circlesCondensed[i][2] < 15:

        if time() > self.targetChange + 5:
            # Find closest food
            targetIndex = 0
            minDist = 1000000
            for i, circle in enumerate(circlesCondensed):
                if circle[2] < 30 and i != usIndex:  # and circle[2] > self.imageCenterY - 150:
                    distToFood = sqrt((float(circle[0]) - USX)**2 + (float(circle[1]) - USY)**2)
                    if distToFood < minDist and distToFood > 1:
                        minDist = distToFood
                        targetIndex = i
            # Compute trajectory
            dY = float(circlesCondensed[targetIndex][1]) - USY
            dX = float(circlesCondensed[targetIndex][0]) - USX

            self.targetChange = time()
            self.lastTarget = atan2(dY, dX) * 180 / pi

        # Making food array
        foodArr = []
        for circle in circlesCondensed:
            if circle[2] < 30 and circle[1] > self.imageCenterY - 150:
                foodArr.append((int(circle[0]) - USX, int(circle[1]) - USY))

        return self.lastTarget, foodArr

    def act(self, image):
        # Create array to store color values read in in
        arr = np.zeros((360 // self.angularRes, self.numRings), dtype=np.int16)
        blobs = np.zeros((360 // self.angularRes, self.numRings), dtype=np.int64)

        for ring in range(self.numRings):
            for θ in range(360 // self.angularRes):
                x = cos(θ * self.angularRes * pi / 180) * (ring * self.radialRes + self.firstRing)
                y = sin(θ * self.angularRes * pi / 180) * (ring * self.radialRes + self.firstRing)
                x += self.imageCenterX
                y += self.imageCenterY
                if x < 0 or x > image.size[0] - 1 or y < self.imageCenterY - 150 or y > image.size[1] - 1:
                    pixelColor = (0, 0, 0)
                else:
                    pixelColor = image.getpixel((x, y))

                # Get hue and saturation out of pixel color
                hsv = colorsys.rgb_to_hsv(pixelColor[0], pixelColor[1], pixelColor[2])
                arr[θ][ring] = -1 if hsv[1] < 0.7 or hsv[2] < 0.9 else hsv[0] * 255

        counts = {}

        # Get the frequency of colors
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if arr[i][j] in counts.keys():
                    counts[arr[i][j]] += 1
                else:
                    counts[arr[i][j]] = 1

        # Blobify everything (danger map)
        for i in range(len(blobs)):
            for j in range(len(blobs[i])):
                blobs[i][j] = 0 if arr[i][j] < 0 else counts[arr[i][j]]
                if blobs[i][j] < 400 / (i + 10)**0.75:  # 250 / (i + 1)**0.75:
                    blobs[i][j] = 0
                else:
                    blobs[i][j] *= 2

        # Get the total blobbed danger in every direction
        dangers = np.zeros(len(blobs))
        for i in range(len(dangers)):
            dangers[i] += np.sum(blobs[i % len(dangers)])

        dangerInDirection = [[], []]
        dangerFound = False
        # Start looking for the direction farthest from any danger
        for i in range(len(dangers)):
            if dangers[i] > 0:
                dangerInDirection[0].append(1)
                dangerInDirection[1].append(1)
                dangerFound = True
            else:
                dangerInDirection[0].append(0)
                dangerInDirection[1].append(0)

        direction = time() * 100
        foodArr = []

        numIterations = 0
        if dangerFound:
            self.targetChange = time() - 100
            while dangerInDirection[numIterations % 2].count(0) > 1:
                for i in range(len(dangers)):
                    if dangerInDirection[numIterations % 2][i - 1] > 0 or \
                            dangerInDirection[numIterations % 2][i] > 0 or \
                            dangerInDirection[numIterations % 2][(i + 1) % len(dangers)] > 0:
                        dangerInDirection[(numIterations + 1) % 2][i] = dangerInDirection[numIterations % 2][i] + 1
                numIterations += 1

            index = 0

            for i in range(len(dangers)):
                if dangerInDirection[numIterations % 2][i] <= 1:
                    index = i
                    break

            direction = index * self.angularRes
        else:
            direction, foodArr = self.__attack__(image)

        # Display the blobbed danger in every direction
        for i in range(len(dangers)):
            blobs[i][0] = 200 - dangerInDirection[numIterations % 2][i] * 10
        self.videoOut.displayFrame(blobs, foodArr)

        return direction
