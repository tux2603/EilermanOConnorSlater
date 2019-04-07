from math import sin, cos
from PIL import Image
import numpy as np


class AI:
    def __init__(self, imageCenterX, imageCenterY):
        self.mode = 'defend'
        self.angularRes = 30
        self.radialRes = 10
        self.numRings = 5
        self.firstRing = 25
        self.imageCenterX = imageCenterX
        self.imageCenterY = imageCenterY

    def recalculateFirstRing(self, image):
        # Set first ring to zero, expand outwards until different color, add res/2
        pass

    def act(self, image):
        if self.mode == 'attack':
            self.attack(image)
        elif self.mode == 'defend':
            self.defend(image)
        else:
            # TODO: Any other modes?
            pass

    def attack(self, image):
        # kill -9 $otherGuy
        pass

    def defend(self, image):
        # Create array to store color values read in in
        arr = np.zeros((360 // self.angularRes, self.numRings), dtype=np.int16)
        radii = [i for i in map(lambda j: j * self.radialRes + self.firstRing, range(self.numRings))]

        for r in radii:
            for θ in range(0, 360 - self.angularRes, self.angularRes):
                print(r, θ)
                x, y = cos(θ) * r, sin(θ) * r

                arr[θ][r] = image.getpixel((self.imageCenterX + x, self.imageCenterY + y))
        print(arr)

if __name__ == '__main__':
    ai = AI(300, 160)
    ai.defend('')
