"""보넷 하드웨어 설정 (화면, 백라이트, 조이스틱·버튼)"""
import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image

WIDTH = 240
HEIGHT = 240

# 버튼 이름 → 핀 (풀업이라 누르면 False)
BUTTON_PINS = {
    "up": board.D17,
    "down": board.D22,
    "left": board.D27,
    "right": board.D23,
    "A": board.D5,
    "B": board.D6,
}


def _make_input(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn


class Hardware:
    def __init__(self):
        # 화면: rotation=0이면 하단이 깨지므로 반드시 180 + y_offset=80
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.CE0)
        dc = digitalio.DigitalInOut(board.D25)
        rst = digitalio.DigitalInOut(board.D24)
        self.disp = st7789.ST7789(
            spi,
            width=WIDTH,
            height=HEIGHT,
            rotation=180,
            y_offset=80,
            cs=cs,
            dc=dc,
            rst=rst,
            baudrate=24000000,
        )

        self.backlight = digitalio.DigitalInOut(board.D26)
        self.backlight.switch_to_output(value=True)

        self.buttons = {}
        for name, pin in BUTTON_PINS.items():
            self.buttons[name] = _make_input(pin)

    def pressed(self, name):
        return not self.buttons[name].value

    def show(self, image):
        self.disp.image(image)

    def cleanup(self):
        self.disp.image(Image.new("RGB", (WIDTH, HEIGHT), "black"))
        self.backlight.value = False