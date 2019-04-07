from math import sin, cos, pi
from PIL import Image, ImageColor
from time import time
import numpy as np
import colorsys
import cv2
from ArrToVideo import VideoOutput


class AI:
    def __init__(self, imageCenterX, imageCenterY):
        self.mode = 'defend'
        self.angularRes = 3
        self.radialRes = 10
        self.numRings = 50
        self.firstRing = 20

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

        dangers = np.zeros(len(arr))
        direction = time()

        for i in range(len(dangers)):
            dangers[i] += 0.25 * np.sum(arr[(i - 2) % len(dangers)])
            dangers[i] += 0.5 * np.sum(arr[(i - 1) % len(dangers)])
            dangers[i] += np.sum(arr[i % len(dangers)])
            dangers[i] += 0.5 * np.sum(arr[(i + 1) % len(dangers)])
            dangers[i] += 0.25 * np.sum(arr[(i + 2) % len(dangers)])

        self.videoOut.displayFrame(arr)

        minDanger = dangers[0]
        minDangerIndex = 0

        for i in range(1,len(dangers)):
            if dangers[i] < minDanger:
                minDanger = dangers[i]
                minDangerIndex = i

        return minDangerIndex * self.angularRes


if __name__ == '__main__':
    ai = AI(300, 260)
    ai.defend('')
