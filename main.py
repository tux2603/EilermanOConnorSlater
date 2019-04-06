import os
import pyautogui as p
import webbrowser
import subprocess
from time import sleep
import Xlib
import Xlib.display
from random import random
from time import time
from threading import Thread
from pynput.mouse import Button, Controller


def openWindow():
    global window, WIDTH, HEIGHT
    os.system('clear')

    # Open the browser
    os.system('firefox -private "https://agar.io" -new-window &')
    sleep(2)

    # Resize the browser
    display = Xlib.display.Display()
    root = display.screen().root

    # Get the x windows ID of the browser
    windowID = root.get_full_property(display.intern_atom(
        '_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]
    window = display.create_resource_object('window', windowID)
    window.configure(width=WIDTH, height=HEIGHT)
    window.set_wm_name("iRobot: prepare to be assimiliated")
    display.sync()
    print(dir(window))
    print(vars(window))


def login():
    # Find and click the play button
    p.moveTo(1, 1)
    while 1:
        loc = p.locateOnScreen(
            'ReferenceImages/playButton.png', confidence=0.9)
        if loc is not None:
            break
    p.moveTo(x=loc.left + 0.5 * loc.width, y=loc.top + 0.5 * loc.height)

    # Type in the name and startt
    p.moveRel(0, -20)
    p.click()
    sleep(0.5 + random())
    p.hotkey('ctrl', 'a')
    sleep(0.5 + random())
    p.typewrite('iRobot', interval=0.5 + random())
    sleep(0.76 + random())
    p.press('enter')
    if SPEAK:
        os.system('espeak -p00 -s80 "I wish to eat you" &')


def deathSound():
    if SPEAK:
        os.system('espeak  -p10 -s150 "oh no... I died!" &')


def captchaSound():
    if SPEAK:
        os.system('espeak  -p10 -s80 "Curses. Foiled again" &')


class DeathChecker(Thread):
    def __init__(self):
        super().__init__()
        self.isDead = False
        self.isDetected = False

    def run(self):
        while 1:
            loc = p.locateOnScreen('ReferenceImages/continueButton.png', confidence=0.9)
            if loc is not None:
                self.isDead = True
                break
            loc = p.locateOnScreen('ReferenceImages/captcha.png', confidence=0.9)
            if loc is not None:
                self.isDetected = True
                break


if __name__ == '__main__':
    WIDTH, HEIGHT = 600, 400
    SPEAK = True
    window = None
    dead = False
    openWindow()
    login()

    # Starting death checking to kill program
    checker = DeathChecker()
    checker.start()

    mouse = Controller()

    # Game Loop
    while not checker.isDead and not checker.isDetected:
        t0 = time()
        mouse.position = (random() * 500, random() * 500)
        sleep(1 / 144)
        print('{} FPS'.format(round(1 / (time() - t0), 3)))

    if checker.isDead:
        deathSound()
    else:
        captchaSound()
    print('we ded')
