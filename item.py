import random
from dungeon import make_floor, ROWS, COLS
from enemy import place_enemies, occupied

# 주황
FUEL_COLOR = (255, 140, 0)
# 파랑
POTION_COLOR = (80, 160, 255)

# 아이템 배치
def place_items(grid, start, enemies, fuel_count, potion_count):
    candidates = []
    for row in range(ROWS):
        for col in range(COLS):
            cell = (row, col)
            if grid[row][col] == "." and cell != start and not occupied(cell, enemies):
                candidates.append(cell)

    cells = random.sample(candidates, fuel_count + potion_count)
    items = []
    for cell in cells[:fuel_count]:
        items.append({"pos": cell, "kind": "fuel"})
    for cell in cells[fuel_count:]:
        items.append({"pos": cell, "kind": "potion"})
    return items

# 그 칸의 아이템 찾기
def item_at(cell, items):
    for item in items:
        if item["pos"] == cell:
            return item
    return None

if __name__ == "__main__":
    grid, start = make_floor()
    enemies = place_enemies(grid, start, 4)
    items = place_items(grid, start, enemies, 2, 1)
    shown = []
    for line in grid:
        shown.append(list(line))
    for item in items:
        if item["kind"] == "fuel":
            shown[item["pos"][0]][item["pos"][1]] = "f"
        else:
            shown[item["pos"][0]][item["pos"][1]] = "p"
    for e in enemies:
        shown[e["pos"][0]][e["pos"][1]] = "E"
    shown[start[0]][start[1]] = "P"
    for line in shown:
        print("".join(line))