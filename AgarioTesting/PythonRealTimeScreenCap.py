# -*- coding: utf-8 -*-
# =============================================================================
# Title: Real-time screen capture
# Author: Ryan J. Slater
# Date: Wed Apr  3 10:22:14 2019
# =============================================================================

from Xlib import display, X
from PIL import Image
from time import time, sleep

W, H = 600, 400
dsp = display.Display()
root = dsp.screen().root

frames = []

NUM_FRAMES = 10000
start = time()
for i in range(NUM_FRAMES):
    raw = root.get_image(0, 0, W, H, X.ZPixmap, 0xffffffff)
    frames.append(Image.frombytes('RGB', (W, H), raw.data, 'raw', 'BGRX'))
stop = time()
print(1 / ((stop - start) / NUM_FRAMES))
