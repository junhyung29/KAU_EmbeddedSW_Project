import random
from dungeon import bfs, make_floor, DIRS, in_vision

ENEMY_HP = 1
ENEMY_COLOR = (220, 60, 60)
MIN_DIST = 3

def place_enemies(grid, start, count):
    dist = bfs(grid, start)
    candidates = []
    for cell in dist:
        if grid[cell[0]][cell[1]] == "." and dist[cell] >= MIN_DIST:
            candidates.append(cell)

    enemies = []
    for cell in random.sample(candidates, count):
        enemies.append({"pos": cell, "hp": ENEMY_HP})
    return enemies

def occupied(cell, enemies):
    for e in enemies:
        if e["pos"] == cell:
            return True
    return False

def move_enemies(grid, pos, enemies, radius):
    dist = bfs(grid, pos)
    for e in enemies:
        if not in_vision(pos, e["pos"], radius):
            continue
        best = e["pos"]
        for dr, dc in DIRS.values():
            nxt = (e["pos"][0] + dr, e["pos"][1] + dc)
            if nxt in dist and nxt != pos and not occupied(nxt, enemies) and dist[nxt] < dist[best]:
                best = nxt
        e["pos"] = best

if __name__ == "__main__":
    grid, start = make_floor()
    enemies = place_enemies(grid, start, 4)
    for turn in range(4):
        shown = []
        for line in grid:
            shown.append(list(line))
        for e in enemies:
            shown[e["pos"][0]][e["pos"][1]] = "E"
        shown[start[0]][start[1]] = "P"
        print("turn", turn)
        for line in shown:
            print("".join(line))
        move_enemies(grid, start, enemies, 99)