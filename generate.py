from dataclasses import dataclass, field
import numpy as np
from random import randint, choice

@dataclass
class MazeCell:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=list)

def find(x):
    global maze
    return maze[x[0]][x[1]].component

def union(x, y):
    global maze
    global components
    x_rank = -1
    y_rank = -1
    for cmpnt in components:
        if cmpnt == maze[x[0]][x[1]].component:
            x_rank += 1
        if cmpnt == maze[y[0]][y[1]].component:
            y_rank += 1
    if x_rank >= y_rank:
        new_component = maze[x[0]][x[1]].component
        old_component = maze[y[0]][y[1]].component
    else:
        new_component = maze[y[0]][y[1]].component
        old_component = maze[x[0]][x[1]].component

    for i in range(len(components)):
        if components[i] == old_component:
            components[i] = new_component
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j].component == old_component:
                maze[i][j].component = new_component

def generate_maze(size) -> list[list[MazeCell]]:
    global maze
    global components
    maze = []
    components = []
    for i in range(size):
        maze.append([])
        for j in range(size):
            maze[i].append(MazeCell(i, j, i * size + j, False, [True, True, True, True]))
            components.append(i * size + j)
    components = np.array(components)

    while len(np.unique(components)) != 1:
        x = randint(0, size - 1)
        y = randint(0, size - 1)
        nbrs = []
        if x != 0:
            nbrs.append([x - 1, y])
        if y != size - 1:
            nbrs.append([x, y + 1])
        if x != size - 1:
            nbrs.append([x + 1, y])
        if y != 0:
            nbrs.append([x, y - 1])
        r_nbr = choice(nbrs)

        if find([x, y]) != find(r_nbr):
            if x > r_nbr[0]:
                maze[x][y].walls[0] = False
                maze[r_nbr[0]][r_nbr[1]].walls[2] = False
            elif y < r_nbr[1]:
                maze[x][y].walls[1] = False
                maze[r_nbr[0]][r_nbr[1]].walls[3] = False
            elif x < r_nbr[0]:
                maze[x][y].walls[2] = False
                maze[r_nbr[0]][r_nbr[1]].walls[0] = False
            elif y > r_nbr[1]:
                maze[x][y].walls[3] = False
                maze[r_nbr[0]][r_nbr[1]].walls[1] = False
            union([x,y], r_nbr)
    maze[0][0].is_open = True
    maze[size - 1][size - 1].is_open = True
    maze[0][0].walls[0] = False
    maze[size - 1][size - 1].walls[2] = False
    return maze

