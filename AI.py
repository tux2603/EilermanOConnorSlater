from math import sin, cos, pi
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
        self.angularRes = 3
        self.radialRes = 10
        self.numRings = 80
        self.firstRing = 25

        self.imageCenterX = imageCenterX
        self.imageCenterY = imageCenterY

        self.videoOut = VideoOutput(self.angularRes, self.radialRes, self.firstRing, self.numRings)

    def recalculateFirstRing(self, image):
        # Set first ring to zero, expand outwards until different color, add res/2
        pass

    def act(self, image):
        direction = time()
        if self.mode == 'attack':
            direction = self.__attack__(image)
        elif self.mode == 'defend':
            direction = self.__defend__(image)
        else:
            # TODO: Any other modes?
            pass
        return direction

    def __attack__(self, image):
        # kill -9 $otherGuy
        pass

    @jit
    def __defend__(self, image):
        # Create array to store color values read in in
        arr = np.zeros((360 // self.angularRes, self.numRings), dtype=np.int16)
        blobs = np.zeros((360 // self.angularRes, self.numRings), dtype=np.int64)

        for ring in range(self.numRings):
            for θ in range(360 // self.angularRes):
                x, y = cos(θ * self.angularRes * pi / 180) * (ring * self.radialRes + self.firstRing), sin(θ * self.angularRes * pi / 180) * (ring * self.radialRes + self.firstRing)
                x += self.imageCenterX
                y += self.imageCenterY
                if x < 0 or x > image.size[0] - 1 or y < self.imageCenterY - 81 or y > image.size[1] - 1:
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
                if blobs[i][j] < 30:
                    blobs[i][j] *= 0

        # Get the total blobbed danger in every direction
        dangers = np.zeros(len(blobs))
        for i in range(len(dangers)):
            dangers[i] += np.sum(blobs[i % len(dangers)])

        # Start looking for the direction farthest from any danger
        dangerInDirection = []
        newDangerInDirection = []
        dangerFound = False

        for i in range(len(dangers)):
            if dangers[i] > 0:
                dangerInDirection.append(1)
                newDangerInDirection.append(1)
                dangerFound = True
            else:
                dangerInDirection.append(0)
                newDangerInDirection.append(0)

        direction = time() * 75

        if dangerFound:
            while dangerInDirection.count(0) > 1:
                for i in range(len(dangers)): newDangerInDirection[i] = dangerInDirection[i]
                for i in range(len(dangers)):
                    if dangerInDirection[i - 1] > 0 or dangerInDirection[i] > 0 or dangerInDirection[(i + 1) % len(dangers)] > 0:
                        newDangerInDirection[i] += 1
                for i in range(len(dangers)): dangerInDirection[i] = newDangerInDirection[i]
                print(dangerInDirection)
            print(50 * "#")

            index = 0

            for i in range(len(dangers)):
                if dangerInDirection[i] <= 1:
                    index = i
                    break

            direction = index * self.angularRes
            print(direction)

        # Display the blobbed danger in every direction
        for i in range(len(dangerInDirection)):
            blobs[i][0] = 200 - dangerInDirection[i] * 10
        self.videoOut.displayFrame(blobs)

        return direction
