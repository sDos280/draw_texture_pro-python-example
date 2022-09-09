from raylib import *
from raylib.colors import *
from pyray import *
import math
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
elementRender: Rectangle = Rectangle(
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
    global sampleSprite, sourceCodeFont, previewElementPre, previewElementResult, codePreviewHighlight
    init_window(screenWidth, screenHeight, "DrawTexturePro Example")
    set_target_fps(60)
    gui_load_style("assets/lavanda.rgs")

    sampleSprite = load_texture("assets/kenney.png")

    sourceCodeFont = load_font_ex("/assets/LiberationMono-Regular.ttf", fontSize, 0, 250)
    # sourceCodeFont = load_font_ex("/assets/Uchen-Regular.ttf", fontSize, 0, 250)

    gui_set_font(sourceCodeFont)
    for j in range(21):
        codePreviewHighlight.append(BEIGE)
        codePreviewHighlight[j] = list(codePreviewHighlight[j])
        codePreviewHighlight[j][3] = 0

    previewElementPre = load_render_texture(
        int(elementRender.width - 20),
        int(elementRender.height - 20)
    )
    previewElementResult = load_render_texture(
        int(elementRender.width - 20),
        int(elementRender.height - 20)
    )

    while not window_should_close():
        # HandleDroppedFiles()

        begin_drawing()
        clear_background(RAYWHITE)

        draw_element_borders()
        setup_difference()
        # DrawUI()
        resolve_mouse_state()
        draw_code_display()

        """
        check_difference()
        draw_output()
        """

        end_drawing()

    close_window()


def draw_element_borders():
    gui_panel(Rectangle(0, 0, screenWidth, screenHeight + 2), "DrawTexturePro Interactive Demo")
    gui_group_box(
        elementSliders,
        "Control Sliders"
    )
    gui_group_box(
        elementCode,
        "Corresponding Code"
    )
    draw_rectangle(
        int(elementCode.x + 10),
        int(elementCode.y + 10),
        int(elementCode.width - 20),
        int(elementCode.height - 20),
        RAYWHITE
    )
    gui_group_box(
        elementPreRender,
        "Source Texture"
    )
    draw_rectangle(
        int(elementPreRender.x + 10),
        int(elementPreRender.y + 10),
        int(elementPreRender.width - 20),
        int(elementPreRender.height - 20),
        RAYWHITE
    )
    gui_group_box(
        elementRender,
        "Rendered Texture"
    )
    draw_rectangle(
        int(elementRender.x + 10),
        int(elementRender.y + 10),
        int(elementRender.width - 20),
        int(elementRender.height - 20),
        RAYWHITE
    )


def setup_difference():
    global predtpSource, predtpDest, predtpOrigin, predtpRotation
    predtpSource = dtpSource
    predtpDest = dtpDest
    predtpOrigin = dtpOrigin
    predtpRotation = dtpRotation


def DrawUI():
    xOffset: int = 60
    yOffset: int = 40
    SLIDER_SPACING: int = 10
    SLIDER_HEIGHT: int = 20
    SLIDER_WIDTH: int = 200


def resolve_mouse_state():
    global dragState, mouseOffset
    # elementRender elementPreRender

    #  if mouse click
    if is_mouse_button_pressed(0):
        #  Source Square
        if check_collision_point_rec(
                get_mouse_position(),
                Rectangle(
                    elementPreRender.x + dtpSource.x + 10 + GRID_CENTER,
                    elementPreRender.y + dtpSource.y + 10 + GRID_CENTER,
                    math.fabs(dtpSource.width),
                    math.fabs(dtpSource.height),
                )):
            gui_lock()
            dragState = DragStates.HeldSource
            mouseOffset = get_mouse_position()
            mouseOffset.x -= elementPreRender.x + dtpSource.x + 10 + GRID_CENTER
            mouseOffset.y -= elementPreRender.y + dtpSource.y + 10 + GRID_CENTER

        # Origin Dot
        elif check_collision_point_circle(
                get_mouse_position(),
                Vector2(
                    elementRender.x - dtpOrigin.x + dtpDest.x + 10 + GRID_CENTER,
                    elementRender.y - dtpOrigin.y + + dtpDest.y + 10 + GRID_CENTER
                ),
                6):
            gui_lock()
            dragState = DragStates.HeldOrigin
            mouseOffset = get_mouse_position()
            mouseOffset.x -= elementRender.x - dtpOrigin.x + (2 * dtpDest.x) + 10 + GRID_CENTER
            mouseOffset.y -= elementRender.y - dtpOrigin.y + (2 * dtpDest.y) + 10 + GRID_CENTER

        # Dest Square
        elif check_collision_point_rec(
                get_mouse_position(),
                Rectangle(
                    elementRender.x + dtpDest.x + 10 + GRID_CENTER,
                    elementRender.y + dtpDest.y + 10 + GRID_CENTER,
                    math.fabs(dtpDest.width),
                    math.fabs(dtpDest.height)
                )):
            gui_lock()
            dragState = DragStates.HeldDest
            mouseOffset = get_mouse_position()
            mouseOffset.x -= elementRender.x + dtpDest.x + 10 + GRID_CENTER
            mouseOffset.y -= elementRender.y + dtpDest.y + 10 + GRID_CENTER

    elif is_mouse_button_down(0):
        if dragState == DragStates.HeldSource:
            dtpSource.x = CLAMP(-mouseOffset.x + get_mouse_x() - (elementPreRender.x + 10 + GRID_CENTER), -192, 192)
            dtpSource.y = CLAMP(-mouseOffset.y + get_mouse_y() - (elementPreRender.y + 10 + GRID_CENTER), -192, 192)
        elif dragState == DragStates.HeldOrigin:
            dtpOrigin.x = CLAMP(-mouseOffset.x - get_mouse_x() + (elementRender.x + 10 + GRID_CENTER), -192, 192)
            dtpOrigin.y = CLAMP(-mouseOffset.y - get_mouse_y() + (elementRender.y + 10 + GRID_CENTER), -192, 192)
        elif dragState == DragStates.HeldDest:
            dtpDest.x = CLAMP(-mouseOffset.x + get_mouse_x() - (elementRender.x + 10 + GRID_CENTER), -192, 192)
            dtpDest.y = CLAMP(-mouseOffset.y + get_mouse_y() - (elementRender.y + 10 + GRID_CENTER), -192, 192)
        elif dragState == DragStates.Released:
            #  shouldn't be possible to reach here
            pass

    elif is_mouse_button_released(0):
        dragState = DragStates.Released
        gui_unlock()

    # if mouse inside square 1, origin, square 2, square 3
    #  set state to move
    # if move state
    #  if inside
    #  move shape
    # if mouse let go: reset state


def draw_code_display():
    codePreviewArray[3] = f"						.x = {int(dtpSource.x)},"
    codePreviewArray[4] = f"						.y = {int(dtpSource.y)},"
    codePreviewArray[5] = f"						.width = {int(dtpSource.width)},"
    codePreviewArray[6] = f"						.height = {int(dtpSource.height)}"
    codePreviewArray[9] = f"						.x = {int(dtpDest.x)},"
    codePreviewArray[10] = f"						.y = {int(dtpDest.y)},"
    codePreviewArray[11] = f"						.width = {int(dtpDest.width)},"
    codePreviewArray[12] = f"						.height = {int(dtpDest.height)}"
    codePreviewArray[15] = f"						.x = {int(dtpOrigin.x)},"
    codePreviewArray[16] = f"						.y = {int(dtpOrigin.y)},"
    codePreviewArray[18] = f"			{int(dtpRotation)}, // Rotation"

    for j in range(21):
        if codePreviewHighlight[j][3] > 0:
            codePreviewHighlight[j][3] -= 5

    for b in range(21):
        tempColor = BLACK
        if (b > 1) and (b < 8):
            tempColor = RED
        elif (b > 7) and (b < 14):
            tempColor = DARKGREEN
        elif (b > 13) and (b < 18):
            tempColor = BLUE
        elif b == 18:
            tempColor = DARKPURPLE

        draw_rectangle(
            int(0 + 20),
            int(elementCode.y + 15 + ((fontSize + 1) * b) - 1),
            int(previewElementResult.texture.width),
            int(fontSize + 1),
            codePreviewHighlight[b]
        )
        draw_text_ex(
            sourceCodeFont,
            codePreviewArray[b],
            Vector2(
                elementCode.x + 15,
                elementCode.y + 15 + ((fontSize + 1) * b)
            ),
            fontSize,
            fontSpacing,
            tempColor
        )


if __name__ == '__main__':
    main()
