import os
import pyautogui as p
import Xlib
import Xlib.display

from math import sin, cos
from time import sleep, time
from PIL import Image
from pynput.mouse import Button, Controller
from random import random
from threading import Thread

from circles import findCircles


def openWindow():
    global window, WIDTH, HEIGHT, display, LEFT, TOP
    os.system('clear')

    # Open the browser
    os.system('firefox "https://agar.io" -new-window -private &')
    sleep(2)

    # Get display
    display = Xlib.display.Display()
    root = display.screen().root

    # Get the x windows ID of the browser
    windowID = root.get_full_property(display.intern_atom('_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]
    window = display.create_resource_object('window', windowID)
    window.configure(width=WIDTH, height=HEIGHT)
    display.sync()

    LEFT, TOP = window.get_geometry().x, window.get_geometry().y


def moveRelAndClick(x, y, delay=0.5):
    p.moveRel(x, y)
    p.click()
    sleep(delay)


def login():
    # Find and click the play button
    p.moveTo(1, 1)
    while 1:
        loc = p.locateOnScreen(
            'ReferenceImages/playButton.png', confidence=0.9)
        if loc is not None:
            break
    p.moveTo(x=loc.left + 0.5 * loc.width, y=loc.top + 0.5 * loc.height)

    # Prep settings

    # Gear Click
    moveRelAndClick(-55, -60)

    # Graphics Click
    moveRelAndClick(0, 10)
    moveRelAndClick(0, 120)

    # Click Pushbutton settings
    moveRelAndClick(3, -2)
    moveRelAndClick(0, -48, 0)
    moveRelAndClick(0, -32, 0)
    moveRelAndClick(0, -16, 0)
    moveRelAndClick(125, -45, 0)

    # Type in the name and start
    p.moveTo(x=loc.left + 0.5 * loc.width, y=loc.top + 0.5 * loc.height)
    p.moveRel(0, -20)
    p.click()
    sleep(0.5 + random())
    p.hotkey('ctrl', 'a')
    sleep(0.5 + random())
    p.typewrite('iRobot', interval=0.5 + random())
    sleep(0.76 + random())
    p.press('enter')
    say("I wish to eat you", 60)
    return ((loc.left + 0.5 * loc.width, loc.top + 0.5 * loc.height))

def say(words, speed=100):
    if SPEAK:
        os.system('espeak -p00 -s{} -k60 "{}" &'.format(speed, words))

def deathSound():
    say("oh no... I DIED!")


def captchaSound():
    say("Curses. Foiled again. I hate bloody captchas")


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


if __name__ == '__main__':
    WIDTH, HEIGHT, TOP, LEFT = 600, 400, 0, 0
    display = None
    SPEAK = False
    window = None
    dead = False

    openWindow()
    playButtonCenter = login()

    # Board dimensions in relation to center of play button
    BOARD_DIMENSIONS = [-300, -82, 600, 300]  # left, top, width, height

    # Calculate the center of the board (x, y)
    centerX = playButtonCenter[0] + BOARD_DIMENSIONS[0] + BOARD_DIMENSIONS[2] / 2
    centerY = playButtonCenter[1] + BOARD_DIMENSIONS[1] + BOARD_DIMENSIONS[3] / 2

    # Starting death checking to kill program
    checker = DeathChecker()
    checker.start()

    mouse = Controller()

    # Game Loop
    while not checker.isDead:
        # Check to make sure google doesn't dislike us
        if checker.isDetected:
            # Ask to solve captcha
            captchaSound()
            window.configure(width=1500, height=900)
            display.sync()
            sleep(1)

            # Wait for captcha to be solved
            while 1:
                if p.locateOnScreen('ReferenceImages/captchaSolve.png', confidence=0.9) is None and p.locateOnScreen('ReferenceImages/captcha.png', confidence=0.9) is None:
                    sleep(1)
                    if p.locateOnScreen('ReferenceImages/captcha.png', confidence=0.9) is None:
                        break
            checker.isDetected = False
            window.configure(width=WIDTH, height=HEIGHT)
            display.sync()

        # Get the image of the screen
        raw = window.get_image(0, 0, WIDTH, HEIGHT, Xlib.X.ZPixmap, 0xffffffff)
        image = Image.frombytes('RGB', (WIDTH, HEIGHT), raw._data['data'], 'raw', 'BGRX')

        # Move in a circle
        mouse.position = (centerX + 150 * cos(time()), centerY + 150 * sin(time()))
        # mouse.position = (random() * 500, random() * 500)
        sleep(1 / 144)

    deathSound()
    print('we ded')
    print(vars(window.get_image(0, 0, 10, 10, Xlib.X.ZPixmap, 0xffffffff)), type(window.get_image(0, 0, WIDTH, HEIGHT, Xlib.X.ZPixmap, 0xffffffff)))
    raw = window.get_image(0, 0, WIDTH, HEIGHT, Xlib.X.ZPixmap, 0xffffffff)
    image = Image.frombytes('RGB', (WIDTH, HEIGHT), raw._data['data'], 'raw', 'BGRX')

    findCircles(image)
    image.show()
