from raylib import *
from pyray import *


def MAX(x, y):
    return x if x > y else y


def MIN(x, y):
    return x if x < y else y


def CLAMP(val, minVal, maxVal):
    return MIN(maxVal, MAX(val, minVal))


screenWidth: int = 900
screenHeight: int = 600

elementMargin: int = 10
elementBorderThickness: int = 3

def main():
    pass

if __name__ == '__main__':
    main()