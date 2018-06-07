import pygame
import random
import time
from Spot import Spot
from Button import Button

current_milli_time = lambda: int(round(time.time() * 1000))

pygame.init()

width = height = 600
width_tot = width + 200

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOW_SIZE = [width_tot, height]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze")

done = False
clock = pygame.time.Clock()

# Setup
cols = rows = 32

allow_diagonals = True
show_visited = False

grid = []
openSet = []
closedSet = []
path = []

saved_path = []

w = width / cols
h = height / rows

for i in range(cols):
    grid.append([])

for i in range(cols):
    for j in range(rows):
        grid[i].append(Spot(i, j, w, h, rows, cols))

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid, allow_diagonals)

start = grid[0][0]
end = grid[cols - 1][rows - 1]
start.wall = False
end.wall = False

# Show buttons
randomize      = Button(width + 25, 30 + 0 * 55, 150, 50, 'Random',     (255, 0, 0))
clear          = Button(width + 25, 30 + 1 * 55, 150, 50, 'Clear',      (0, 0, 255))
start          = Button(width + 25, 30 + 3 * 55, 150, 50, 'A*',         (255, 5, 250))
start_bfs      = Button(width + 25, 30 + 4 * 55, 150, 50, 'BFS',        (255, 5, 250))
start_path     = Button(width + 25, 30 + 6 * 55, 150, 50, 'A* + PATH',  (255, 5, 250))
start_bfs_path = Button(width + 25, 30 + 7 * 55, 150, 50, 'BFS + PATH', (255, 5, 250))


def clear_grid():
    global openSet
    global closedSet
    global saved_path
    saved_path = []
    for i in range(rows):
        for j in range(cols):
            grid[i][j].wall = False
    openSet = []
    closedSet = []


def randomize_grid():
    clear_grid()
    for i in range(rows):
        for j in range(cols):
            if random.random() < 0.3:
                grid[i][j].wall = True
    grid[0][0].wall = False
    grid[rows - 1][cols - 1].wall = False


start_enable = False
start_enable_rec = False


def start_general():
    global openSet
    global closedSet
    global path
    openSet = []
    closedSet = []
    path = []
    start = grid[0][0]
    openSet.append(start)
    end = grid[cols - 1][rows - 1]
    start.wall = False
    end.wall = False


def start_grid():
    start_general()
    global start_enable
    start_enable = True


def start_grid_bfs():
    start_general()
    global start_enable_rec
    start_enable_rec = True


time_start = 0

hold = False
# Game loop
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [sprite for r in grid for sprite in r if sprite.rect.collidepoint(pos)]

            if clear.rect.collidepoint(pos) > 0:
                hold = False
                clear_grid()

            if randomize.rect.collidepoint(pos) > 0:
                hold = False
                randomize_grid()

            if start.rect.collidepoint(pos) > 0:
                time_start = current_milli_time()
                hold = False
                show_visited = False
                start_grid()

            if start_bfs.rect.collidepoint(pos) > 0:
                time_start = current_milli_time()
                hold = False
                show_visited = False
                start_grid_bfs()

            if start_path.rect.collidepoint(pos) > 0:
                time_start = current_milli_time()
                hold = False
                show_visited = True
                start_grid()

            if start_bfs_path.rect.collidepoint(pos) > 0:
                time_start = current_milli_time()
                hold = False
                show_visited = True
                start_grid_bfs()

            if len(clicked_sprites) > 0:
                # print(pos)
                clicked_sprites[0].wall = True
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [sprite for r in grid for sprite in r if sprite.rect.collidepoint(pos)]

            if len(clicked_sprites) > 0:
                clicked_sprites[0].wall = False

    if hold:
        continue

    if start_enable_rec:
        if len(openSet) > 0:
            current = openSet[0]

            if current == end:
                print('Done in ', (current_milli_time() - time_start), ' milliseconds!')
                hold = True
                start_enable_rec = False
                saved_path = path

            openSet.remove(current)

            neighbors = current.neighbors
            for i in range(len(neighbors)):
                neighbor = neighbors[i]
                if neighbor not in closedSet and not neighbor.wall:
                    if neighbor not in openSet:
                        openSet.append(neighbor)
                        closedSet.append(neighbor)
                    neighbor.previous = current
            closedSet.append(current)
        else:
            print('No solution')
            pygame.event.wait()
            break

    if start_enable:
        if len(openSet) > 0:
            winner = 0
            for i in range(len(openSet)):
                if openSet[i].f < openSet[winner].f:
                    winner = i

            current = openSet[winner]

            if current == end:
                print('Done in ', (current_milli_time() - time_start), ' milliseconds!')
                hold = True
                start_enable = False
                saved_path = path

            openSet.remove(current)
            closedSet.append(current)

            neighbors = current.neighbors
            for i in range(len(neighbors)):
                neighbor = neighbors[i]
                if neighbor not in closedSet and not neighbor.wall:
                    tempG = current.g + 1

                    newPath = False
                    if neighbor in openSet:
                        if tempG < neighbor.g:
                            neighbor.g = tempG
                            newPath = True
                    else:
                        neighbor.g = tempG
                        openSet.append(neighbor)
                        newPath = True
                    if newPath:
                        neighbor.h = Spot.heuristic(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.previous = current
        else:
            print('No solution')
            pygame.event.wait()
            break

    screen.fill(BLACK)

    randomize.show(screen)
    clear.show(screen)
    start.show(screen)
    start_bfs.show(screen)
    start_path.show(screen)
    start_bfs_path.show(screen)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].show(screen, WHITE)

    if start_enable_rec or start_enable:
        # Find path
        path = []
        temp = current
        path.append(temp)
        while temp.previous:
            path.append(temp.previous)
            temp = temp.previous
        path.append(temp)
        temp.show(screen, BLUE)
        for i in range(len(path)):
            path[i].show(screen, BLUE)
    else:
        for i in range(len(saved_path)):
            saved_path[i].show(screen, BLUE)


    if show_visited:
        for i in range(len(closedSet)):
            closedSet[i].show(screen, RED)

        for i in range(len(openSet)):
            openSet[i].show(screen, GREEN)

    # clock.tick(60)
    pygame.display.flip()

pygame.quit()
