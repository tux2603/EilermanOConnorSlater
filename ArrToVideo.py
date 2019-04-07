import pygame
import numpy as np
import colorsys
import os
from math import sin, cos, pi
from numba import jit


class VideoOutput:
    def __init__(self, angularRes, radialRes, firstRing, numRings):
        self.angularRes = angularRes
        self.radialRes = radialRes
        self.firstRing = firstRing
        self.numRings = numRings

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1120, 100)
        pygame.init()
        self.display = pygame.display.set_mode((500, 500))

    @jit
    def displayFrame(self, arr):
        # Generate blips
        circleRadius = 1
        rFactor = 4

        for θ in range(len(arr)):
            for ring in range(len(arr[θ])):
                if (ring < 50 and θ % 1 == 0) or False:
                    hsv = (0, 0, 0) if arr[θ][ring] < 0 else (arr[θ][ring] / 255, 1, 255)

                    rFactor = 2
                    x = 250 + int(cos(θ * self.angularRes * pi / 180) * (ring * rFactor + self.firstRing))
                    y = 250 + int(sin(θ * self.angularRes * pi / 180) * (ring * rFactor + self.firstRing))

                    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
                    intRGB = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
                    pygame.draw.circle(self.display, intRGB, (x, y), circleRadius)

        # Update display
        pygame.display.update()
