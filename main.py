# 게임 뼈대 파일
import time

from PIL import Image, ImageDraw

from hw import Hardware, WIDTH, HEIGHT

# 루프를 한 번 돌 때마다 쉬는 시간(초). 너무 짧으면 CPU를 많이 쓴다.
FRAME_DELAY = 0.05


def draw_frame(pressed_names):
    """이번 화면을 그려서 PIL 이미지로 돌려준다."""
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    draw.text((10, 10), "The Last Torch", fill="white")

    if pressed_names:
        text = " ".join(pressed_names)
    else:
        text = "(none)"
    draw.text((10, 40), "pressed: " + text, fill="yellow")

    return image


def main():
    hw = Hardware()
    try:
        while True:
            # 눌려 있는 버튼 이름을 모은다
            pressed_names = []
            for name in hw.buttons:
                if hw.pressed(name):
                    pressed_names.append(name)

            image = draw_frame(pressed_names)
            hw.show(image)

            time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        # Ctrl+C로 끝낸 경우. 에러가 아니므로 조용히 넘어간다.
        pass
    finally:
        # 정상 종료든 에러든 화면을 정리한다.
        hw.cleanup()


if __name__ == "__main__":
    main()