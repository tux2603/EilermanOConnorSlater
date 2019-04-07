import pygame
import numpy as np
import colorsys
import os
from math import sin, cos, pi


class VideoOutput:
    def __init__(self, angularRes, radialRes, firstRing, numRings):
        self.angularRes = angularRes
        self.radialRes = radialRes
        self.firstRing = firstRing
        self.numRings = numRings

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1920 - 500, 100)
        pygame.init()
        self.display = pygame.display.set_mode((500, 500))

    def displayFrame(self, arr):
        # Generate blips
        circleRadius = 1

        for θ in range(len(arr)):
            for ring in range(len(arr[θ])):
                if θ % 3 == 0 or True:
                    hsv = (0, 0, 0) if arr[θ][ring] < 0 else (arr[θ][ring] / 255, 1, 255)

                    x = 250 + int(cos(θ * self.angularRes * pi / 180) * (ring * self.radialRes + self.firstRing))
                    y = 250 + int(sin(θ * self.angularRes * pi / 180) * (ring * self.radialRes + self.firstRing))

                    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
                    intRGB = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
                    pygame.draw.circle(self.display, intRGB, (x, y), circleRadius)

        # Update display
        pygame.display.update()
