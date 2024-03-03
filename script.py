import os
import time
import keyboard

# Loads The CubeTheSphere.exe
def load():
        temp = os.getenv('TEMP')
        os.startfile(temp+ '\\cspr\\CubeTheSphere.exe')
        keyboard.press_and_release('Alt')
        keyboard.press_and_release('Enter')
        keyboard.press_and_release('Enter')
        keyboard.press_and_release('Ctrl+A')
        time.sleep(0.5)

#==========================================#
# Resolution Settings Based O User's Input #
#==========================================#

def res256():
        keyboard.press_and_release('Enter')
        time.sleep(1)
        keyboard.press_and_release('Alt')
        time.sleep(1)
        keyboard.press_and_release('Right')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Enter')

def res512():
        keyboard.press_and_release('Enter')
        time.sleep(1)
        keyboard.press_and_release('Alt')
        time.sleep(1)
        keyboard.press_and_release('Right')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Enter')

def res1024():
        keyboard.press_and_release('Enter')
        time.sleep(1)
        keyboard.press_and_release('Alt')
        time.sleep(1)
        keyboard.press_and_release('Right')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Enter')
        
def res2048():
        keyboard.press_and_release('Enter')
        time.sleep(1)
        keyboard.press_and_release('Alt')
        time.sleep(1)
        keyboard.press_and_release('Right')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Down')
        time.sleep(0.5)
        keyboard.press_and_release('Enter')

def extractall():
        keyboard.press_and_release('Alt')
        keyboard.press_and_release('Enter')
        keyboard.press_and_release('Down')
        keyboard.press_and_release('Enter')

def extractdone():
        keyboard.press_and_release('Alt+F4')