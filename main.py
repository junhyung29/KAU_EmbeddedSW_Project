# 게임 뼈대 파일
import math
import time
from PIL import Image, ImageDraw
from dungeon import make_map, DIRS, TILE, COLS, ROWS, INFO_H, WALL_COLOR, FLOOR_COLOR, PLAYER_COLOR
from hw import Hardware, WIDTH, HEIGHT

# 루프를 한 번 돌 때마다 쉬는 시간(초)
FRAME_DELAY = 0.05
FUEL_MAX = 50
FUEL_PER_RADIUS = 10

def vision_radius(fuel):
    return math.ceil(fuel / FUEL_PER_RADIUS)

def draw_map(draw, grid, pos, radius):
    for row in range(ROWS):
        for col in range(COLS):
            dr, dc = row - pos[0], col - pos[1]
            if dr * dr + dc * dc > radius * radius + radius:
                continue
            x = col * TILE
            y = INFO_H + row * TILE
            if grid[row][col] == "#":
                color = WALL_COLOR
            else:
                color = FLOOR_COLOR
            draw.rectangle((x, y, x + TILE - 1, y + TILE - 1), fill=color)
            
def draw_frame(pos, grid, fuel):
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    draw_map(draw, grid, pos, vision_radius(fuel))
    x, y = pos[1] * TILE, INFO_H + pos[0] * TILE
    draw.rectangle((x + 3, y + 3, x + TILE - 4, y + TILE - 4), fill=PLAYER_COLOR)

    # 정보창은 y=0~31 안에 들어와야 한다
    draw.text((4, 4), "The Last Torch", fill="white")
    draw.text((4, 18), f"fuel: {fuel}/{FUEL_MAX}", fill="yellow")

    return image


def main():
    hw = Hardware()
    grid, pos = make_map()
    prev = None  # 지난 프레임에 고른 방향 (None = 중립)
    fuel = FUEL_MAX
    try:
        while True:
            # 눌려 있는 버튼 이름을 모은다
            pressed_names = []
            for name in hw.buttons:
                if hw.pressed(name):
                    pressed_names.append(name)

            d = None
            for direction in DIRS:
                if direction in pressed_names:
                    d = direction
                    break   
            if d and not prev:  
                r, c = pos[0] + DIRS[d][0], pos[1] + DIRS[d][1]
                if grid[r][c] != "#":
                    pos = (r, c)
                    if fuel > 0:
                        fuel -= 1
            prev = d

            image = draw_frame(pos, grid, fuel)
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