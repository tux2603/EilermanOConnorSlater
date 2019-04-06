import os
import pyautogui as p
import webbrowser
import subprocess
from time import sleep
import Xlib
import Xlib.display
from random import random


def openWindow():
    os.system('clear')
    # Window Size
    WIDTH, HEIGHT = 600, 400

    # Open the browser
    os.system('firefox -private "https://agar.io" -new-window &')
    sleep(2)

    # Resize the browser
    display = Xlib.display.Display()
    root = display.screen().root

    # Get the x windows ID of the browser
    windowID = root.get_full_property(display.intern_atom('_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]
    window = display.create_resource_object('window', windowID)
    window.configure(width=WIDTH, height=HEIGHT)
    display.sync()
    print(dir(window))
    print(vars(window))
    # print(window.get_image())
    # print(window.get_geometry())


def login():
    # Find and click the play button
    p.moveTo(1, 1)
    while 1:
        loc = p.locateOnScreen('ReferenceImages/playButton.png', confidence=0.9)
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


def findContinueButton():
    return p.locateOnScreen('ReferenceImages/continueButton.png', confidence=0.9)


def clickContinue():
    # Find and click the continue button
    while 1:
        loc = findContinueButton()
        if loc is not None:
            break
    p.moveTo(x=loc.left + 0.5 * loc.width, y=loc.top + 0.5 * loc.height)
    p.click()


if __name__ == '__main__':
    openWindow()
    login()
    # Game Loop
    while 1:
        if findContinueButton() is not None:
            break

        p.moveTo(random() * 500, random() * 500)
    os.system('espeak "oh no... I died!"')
