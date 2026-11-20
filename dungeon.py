import random
from collections import deque

TILE = 16
COLS = 15
ROWS = 13
INFO_H = 32

WALL_COLOR = (120, 120, 140)
FLOOR_COLOR = (50, 35, 25)
PLAYER_COLOR = (255, 200, 60)
STAIRS_COLOR = (80, 200, 120)

DIRS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

ROOM_TRIES = 30   # 방을 생성해보는 횟수
ROOM_MIN = 3      # 방 한 변의 최소/최대 칸 수
ROOM_MAX = 5
MIN_ROOMS = 4     # 방의 최소 개수


def overlaps_any(room, rooms):
    # 방: (행, 열, 행 개수, 열 개수), 방 사이에 벽이 한 칸은 남아야 하므로 끝을 한 칸 늘려서 비교
    r, c, h, w = room
    for r2, c2, h2, w2 in rooms:
        if r < r2 + h2 + 1 and r2 < r + h + 1 and c < c2 + w2 + 1 and c2 < c + w + 1:
            return True
    return False


def center(room):
    return (room[0] + room[2] // 2, room[1] + room[3] // 2)

# 시작 칸에서 이동할 수 있는 칸들을 모두 찾고, 각 칸까지 몇 걸음인지 알려줌
def bfs(grid, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRS.values():
            nr, nc = r + dr, c + dc
            if grid[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                queue.append((nr, nc))
    return dist

def in_vision(pos, cell, radius):
    dr, dc = cell[0] - pos[0], cell[1] - pos[1]
    return dr * dr + dc * dc <= radius * radius + radius

# 맵 생성 함수
def make_map():
    while True:
        grid = []
        for _ in range(ROWS):
            grid.append(["#"] * COLS)

        rooms = []
        # 현재 맵에 사용할 방 정함
        for _ in range(ROOM_TRIES):
            h = random.randint(ROOM_MIN, ROOM_MAX)
            w = random.randint(ROOM_MIN, ROOM_MAX)
            room = (random.randint(1, ROWS - 1 - h), random.randint(1, COLS - 1 - w), h, w)
            if not overlaps_any(room, rooms):
                rooms.append(room)
        if len(rooms) < MIN_ROOMS:
            continue
        
        rooms.sort()
        for r, c, h, w in rooms:
            for i in range(r, r + h):
                for j in range(c, c + w):
                    grid[i][j] = "."

        for k in range(len(rooms) - 1):
            r1, c1 = center(rooms[k])
            r2, c2 = center(rooms[k + 1])
            for col in range(min(c1, c2), max(c1, c2) + 1):
                grid[r1][col] = "."
            for row in range(min(r1, r2), max(r1, r2) + 1):
                grid[row][c2] = "."

        # 검사
        start = center(rooms[0])
        floors = 0
        for line in grid:
            floors += line.count(".")
        if len(bfs(grid, start)) == floors:
            return grid, start
        
def make_floor():
    grid, start = make_map()
    dist = bfs(grid, start)
    far = start
    
    for cell in dist:
        if dist[cell] > dist[far]:
            far = cell    
            
    grid[far[0]][far[1]] = ">"
    return grid, start

if __name__ == "__main__":
    grid, start = make_floor()
    for line in grid:
        print("".join(line))
    print("start:", start)