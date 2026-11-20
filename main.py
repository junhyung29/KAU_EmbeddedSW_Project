# 게임 뼈대 파일
import math
import time
from PIL import Image, ImageDraw
from dungeon import make_floor, DIRS, TILE, COLS, ROWS, INFO_H, WALL_COLOR, FLOOR_COLOR, PLAYER_COLOR, STAIRS_COLOR
from hw import Hardware, WIDTH, HEIGHT
from enemy import place_enemies, ENEMY_COLOR

# 루프를 한 번 돌 때마다 쉬는 시간(초)
FRAME_DELAY = 0.05
FUEL_MAX = 50
FUEL_PER_RADIUS = 10
START_FLOOR = 1
FINAL_FLOOR = 3
ENEMIES_PER_FLOOR = {1: 2, 2: 4, 3: 0}

def vision_radius(fuel):
    return math.ceil(fuel / FUEL_PER_RADIUS)

def in_vision(pos, cell, radius):
    dr, dc = cell[0] - pos[0], cell[1] - pos[1]
    return dr * dr + dc * dc <= radius * radius + radius

def draw_map(draw, grid, pos, radius):
    for row in range(ROWS):
        for col in range(COLS):
            if not in_vision(pos, (row, col), radius):
                continue
            x = col * TILE
            y = INFO_H + row * TILE
            if grid[row][col] == "#":
                color = WALL_COLOR
            elif grid[row][col] == ">":
                color = STAIRS_COLOR
            else:
                color = FLOOR_COLOR
            draw.rectangle((x, y, x + TILE - 1, y + TILE - 1), fill=color)
            
def draw_frame(pos, grid, fuel, floor, enemies):
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    radius = vision_radius(fuel)
    draw_map(draw, grid, pos, radius)
    
    for e in enemies:
        if in_vision(pos, e["pos"], radius):
            ex, ey = e["pos"][1] * TILE, INFO_H + e["pos"][0] * TILE
            draw.rectangle((ex + 3, ey + 3, ex + TILE - 4, ey + TILE - 4), fill=ENEMY_COLOR)
            
    x, y = pos[1] * TILE, INFO_H + pos[0] * TILE
    draw.rectangle((x + 3, y + 3, x + TILE - 4, y + TILE - 4), fill=PLAYER_COLOR)

    # 정보창은 y=0~31 안에 들어와야 한다
    draw.text((4, 4), "The Last Torch", fill="white")
    draw.text((4, 18), f"floor: {floor}  fuel: {fuel}/{FUEL_MAX}", fill="yellow")

    return image


def main():
    hw = Hardware()
    grid, pos = make_floor()
    prev = None  # 지난 프레임에 고른 방향 (None = 중립)
    fuel = FUEL_MAX
    floor = START_FLOOR
    enemies = place_enemies(grid, pos, ENEMIES_PER_FLOOR[floor])
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
                    if grid[r][c] == ">" and floor < FINAL_FLOOR:
                        floor += 1
                        grid, pos = make_floor()
                        enemies = place_enemies(grid, pos, ENEMIES_PER_FLOOR[floor])
            prev = d

            image = draw_frame(pos, grid, fuel, floor, enemies)
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