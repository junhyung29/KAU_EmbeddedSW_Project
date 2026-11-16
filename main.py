# 게임 뼈대 파일
import time
from PIL import Image, ImageDraw
from dungeon import MAP, TILE, COLS, ROWS, INFO_H, WALL_COLOR, FLOOR_COLOR, PLAYER_COLOR, START
from hw import Hardware, WIDTH, HEIGHT

# 루프를 한 번 돌 때마다 쉬는 시간(초). 너무 짧으면 CPU를 많이 쓴다.
FRAME_DELAY = 0.05

# 방향 : (행, 열)
DIRS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def draw_map(draw):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE
            y = INFO_H + row * TILE
            if MAP[row][col] == "#":
                color = WALL_COLOR
            else:
                color = FLOOR_COLOR
            draw.rectangle((x, y, x + TILE - 1, y + TILE - 1), fill=color)
            
def draw_frame(pressed_names, pos):
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    draw_map(draw)
    x, y = pos[1] * TILE, INFO_H + pos[0] * TILE
    draw.rectangle((x + 3, y + 3, x + TILE - 4, y + TILE - 4), fill=PLAYER_COLOR)

    # 정보창은 y=0~31 안에 들어와야 한다
    draw.text((4, 4), "The Last Torch", fill="white")
    if pressed_names:
        text = " ".join(pressed_names)
    else:
        text = "(none)"
    draw.text((4, 18), "pressed: " + text, fill="yellow")

    return image


def main():
    hw = Hardware()
    pos = START
    prev = None  # 지난 프레임에 고른 방향 (None = 중립)
    try:
        while True:
            # 눌려 있는 버튼 이름을 모은다
            pressed_names = []
            for name in hw.buttons:
                if hw.pressed(name):
                    pressed_names.append(name)

            d = next((n for n in DIRS if n in pressed_names), None)
            if d and not prev:
                r, c = pos[0] + DIRS[d][0], pos[1] + DIRS[d][1]
                if MAP[r][c] != "#":
                    pos = (r, c)
            prev = d

            image = draw_frame(pressed_names, pos)
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