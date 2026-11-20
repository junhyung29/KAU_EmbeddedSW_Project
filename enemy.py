import random
from dungeon import bfs, make_floor

ENEMY_HP = 1
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

if __name__ == "__main__":
    grid, start = make_floor()
    for e in place_enemies(grid, start, 4):
        grid[e["pos"][0]][e["pos"][1]] = "E"
    for line in grid:
        print("".join(line))
    print("start:", start)