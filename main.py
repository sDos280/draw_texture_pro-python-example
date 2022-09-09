from raylib import *
from pyray import *
from enum import Enum, auto


def CLAMP(VAL, MIN, MAX):
    return min(MAX, max(VAL, MIN))


screenWidth: int = 900
screenHeight: int = 600

elementMargin: int = 10
elementBorderThickness: int = 3

elementSliders: Rectangle = Rectangle(
    elementMargin,
    28 + elementMargin,
    screenWidth - (elementMargin * 2),
    (screenHeight / 3) - elementMargin - 28
)
elementCode: Rectangle = Rectangle(
    elementMargin,
    (screenHeight / 3) + elementMargin + 8,
    (screenWidth / 3) - elementMargin,
    ((2 * screenHeight) / 3) - (elementMargin * 2) - 8
)
elementPreRender: Rectangle = Rectangle(
    (screenWidth / 3) + (elementMargin / 2),
    (screenHeight / 3) + elementMargin + 8,
    (screenWidth / 3) - elementMargin,
    ((2 * screenHeight) / 3) - (elementMargin * 2) - 8
)
elementRender: Rectangle = (
    ((2 * screenWidth) / 3),
    (screenHeight / 3) + elementMargin + 8,
    (screenWidth / 3) - elementMargin,
    ((2 * screenHeight) / 3) - (elementMargin * 2) - 8
)
sourceCodeFont: Font = Font()
fontSize: int = 14
fontSpacing: int = 0


class DragStates(Enum):
    Released = auto()
    HeldSource = auto()
    HeldDest = auto(),
    HeldOrigin = auto()


dragState: DragStates = DragStates.Released
mouseOffset: Vector2 = Vector2(0, 0)

codePreviewArray: list[str] = [
    "DrawTexturePro(",
    "			texture,",
    "			(Rectangle) { // Source Rectangle",
    "", "", "", "",  # 3-6 are filled out dynamically
    "			},",
    "			(Rectangle) { // Dest Rectangle",
    "", "", "", "",  # 9-12 are filled out dynamically
    "			},",
    "			(Vector2) { // Origin",
    "", "",  # 15-16 are filled out dynamically
    "			},",
    "",  # 18 is filled out dynamically
    "			WHITE // Color",
    ");"
]

i: int = 0
codePreviewHighlight: list[Color] = []

# dtp mean draw texture pro
predtpSource: Rectangle = Rectangle()
dtpSource: Rectangle = Rectangle(
    0,
    0,
    48,
    48
)
predtpDest: Rectangle = Rectangle()
dtpDest: Rectangle = Rectangle(
    0,
    0,
    96,
    96
)
predtpOrigin: Vector2 = Vector2()
dtpOrigin: Vector2 = Vector2(
    0,
    0
)
predtpRotation: int = int()
dtpRotation: int = 0

GRID_SIZE: int = 20
GRID_CENTER: int = 20

sampleSprite: Texture = Texture()
previewElementPre: RenderTexture = RenderTexture()
previewElementResult: RenderTexture = RenderTexture()


def main():
    pass

if __name__ == '__main__':
    main()
