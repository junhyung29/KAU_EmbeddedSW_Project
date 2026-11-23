# 게임 뼈대 파일
import math
import time
import random
from PIL import Image, ImageDraw
from dungeon import make_floor, DIRS, TILE, COLS, ROWS, INFO_H, WALL_COLOR, FLOOR_COLOR, PLAYER_COLOR, STAIRS_COLOR, in_vision
from hw import Hardware, WIDTH, HEIGHT
from enemy import place_enemies, ENEMY_COLOR, move_enemies, enemy_at
from item import place_items, FUEL_COLOR, POTION_COLOR, item_at

# 루프를 한 번 돌 때마다 쉬는 시간(초)
FRAME_DELAY = 0.05
FUEL_MAX = 50
FUEL_PER_RADIUS = 10
START_FLOOR = 1
FINAL_FLOOR = 3
PLAYER_HP_MAX = 3
ENEMIES_PER_FLOOR = {1: 2, 2: 4, 3: 0}
FUEL_ITEMS_PER_FLOOR = 2
MAX_POTIONS_PER_FLOOR = 1
FUEL_PICKUP = 10
POTION_CARRY_MAX = 2

def vision_radius(fuel):
    return math.ceil(fuel / FUEL_PER_RADIUS)

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
            
def draw_frame(pos, grid, fuel, floor, enemies, hp, items, potions):
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    radius = vision_radius(fuel)
    draw_map(draw, grid, pos, radius)
 
    for item in items:
        if in_vision(pos, item["pos"], radius):
            ix, iy = item["pos"][1] * TILE, INFO_H + item["pos"][0] * TILE
            if item["kind"] == "fuel":
                color = FUEL_COLOR
            else:
                color = POTION_COLOR
            draw.rectangle((ix + 5, iy + 5, ix + TILE - 6, iy + TILE - 6), fill=color)    
    
    for e in enemies:
        if in_vision(pos, e["pos"], radius):
            ex, ey = e["pos"][1] * TILE, INFO_H + e["pos"][0] * TILE
            draw.rectangle((ex + 3, ey + 3, ex + TILE - 4, ey + TILE - 4), fill=ENEMY_COLOR)
            
    x, y = pos[1] * TILE, INFO_H + pos[0] * TILE
    draw.rectangle((x + 3, y + 3, x + TILE - 4, y + TILE - 4), fill=PLAYER_COLOR)

    # 정보창은 y=0~31 안에 들어와야 한다
    draw.text((4, 4), f"The Last Torch  hp: {hp}/{PLAYER_HP_MAX}", fill="white")
    draw.text((4, 18), f"floor: {floor}  fuel: {fuel}/{FUEL_MAX} potion: {potions}", fill="yellow")

    return image


def main():
    hw = Hardware()
    grid, pos = make_floor()
    prev = None  # 지난 프레임에 고른 방향 (None = 중립)
    fuel = FUEL_MAX
    hp = PLAYER_HP_MAX
    floor = START_FLOOR
    potions = 0
    enemies = place_enemies(grid, pos, ENEMIES_PER_FLOOR[floor])
    potion_count = random.randint(0, MAX_POTIONS_PER_FLOOR)
    items = place_items(grid, pos, enemies, FUEL_ITEMS_PER_FLOOR, potion_count)    
    try:
        while True:
            # 눌려 있는 버튼 이름을 모은다
            pressed_names = []
            for name in hw.buttons:
                if hw.pressed(name):
                    pressed_names.append(name)

            action = None
            for direction in DIRS:
                if direction in pressed_names:
                    action = direction
                    break   
                
            turn_used = False
            if action and not prev:
                r, c = pos[0] + DIRS[action][0], pos[1] + DIRS[action][1]
                if grid[r][c] != "#":
                    target = enemy_at((r, c), enemies)
                    if target:
                        target["hp"] -= 1
                        if target["hp"] <= 0:
                            enemies.remove(target)
                    else:
                        pos = (r, c)
                    turn_used = True
            if turn_used:
                if fuel > 0:
                    fuel -= 1
                    
                item = item_at(pos, items)
                if item:
                    if item["kind"] == "fuel":
                        fuel = min(fuel + FUEL_PICKUP, FUEL_MAX)
                        items.remove(item)
                    elif potions < POTION_CARRY_MAX:
                        potions += 1
                        items.remove(item)    
                        
                if grid[pos[0]][pos[1]] == ">" and floor < FINAL_FLOOR:
                    floor += 1
                    grid, pos = make_floor()
                    enemies = place_enemies(grid, pos, ENEMIES_PER_FLOOR[floor])
                    potion_count = random.randint(0, MAX_POTIONS_PER_FLOOR)
                    items = place_items(grid, pos, enemies, FUEL_ITEMS_PER_FLOOR, potion_count)
                else:
                    damage = move_enemies(grid, pos, enemies, vision_radius(fuel))
                    hp = max(0, hp - damage)
            prev = action

            image = draw_frame(pos, grid, fuel, floor, enemies, hp, items, potions)
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