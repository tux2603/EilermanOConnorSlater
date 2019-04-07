from math import sin, cos, pi
from PIL import Image, ImageColor
from time import time
import numpy as np
import collections
import colorsys
import cv2
from ArrToVideo import VideoOutput


class AI:
    def __init__(self, imageCenterX, imageCenterY):
        self.mode = 'defend'
        self.angularRes = 1
        self.radialRes = 5
        self.numRings = 30
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

        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if arr[i][j] in counts.keys():
                    counts[arr[i][j]] += 1
                else:
                    counts[arr[i][j]] = 1

        for i in range(len(blobs)):
            for j in range(len(blobs[i])):
                blobs[i][j] = 0 if arr[i][j] < 0 else counts[arr[i][j]]
                if blobs[i][j] < 70:
                    blobs[i][j] *= -0.5
                else:
                    blobs[i][j] **= 4

        dangers = np.zeros(len(blobs))
        direction = time()

        for i in range(len(dangers)):
            dangers[i] += 0.25 * np.sum(blobs[(i - 4) % len(dangers)])
            dangers[i] += 0.25 * np.sum(blobs[(i - 3) % len(dangers)])
            dangers[i] += 0.25 * np.sum(blobs[(i - 2) % len(dangers)])
            dangers[i] += 0.5 * np.sum(blobs[(i - 1) % len(dangers)])
            dangers[i] += np.sum(blobs[i % len(dangers)])
            dangers[i] += 0.5 * np.sum(blobs[(i + 1) % len(dangers)])
            dangers[i] += 0.25 * np.sum(blobs[(i + 2) % len(dangers)])
            dangers[i] += 0.25 * np.sum(blobs[(i + 3) % len(dangers)])
            dangers[i] += 0.25 * np.sum(blobs[(i + 4) % len(dangers)])

        for i in range(len(dangers)):
            blobs[i][0] = (dangers[i] + 70) / 200

        self.videoOut.displayFrame(blobs)

        maxDanger = dangers[0]
        maxDangerIndex = 0

        for i in range(1, len(dangers)):
            if dangers[i] > maxDanger:
                maxDanger = dangers[i]
                maxDangerIndex = i

        return maxDangerIndex * self.angularRes + 180


if __name__ == '__main__':
    ai = AI(300, 260)
    ai.defend('')
