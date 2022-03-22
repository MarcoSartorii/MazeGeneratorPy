import random
import tkinter
from enum import Enum

SEED = random.randint(0, 1000)
random.seed(SEED)

WIDTH = 1000
HEIGHT = 700
N_W_CELLS = 50
N_H_CELLS = 35
N_BOSS_ROOMS = 10
W_CELL = WIDTH / N_W_CELLS
H_CELL = HEIGHT / N_H_CELLS


class AvailableNeighbours(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class CellType(Enum):
    SPAWN = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    END = 5
    BOSS = 6


class Border(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


def get_borders(i, j):
    lst = [Border.LEFT, Border.RIGHT, Border.DOWN, Border.UP]
    if board[i][j] == CellType.UP or (j > 0 and board[i][j - 1] == CellType.DOWN):
        lst.remove(Border.UP)
    if board[i][j] == CellType.DOWN or (j < N_H_CELLS - 1 and board[i][j + 1] == CellType.UP):
        lst.remove(Border.DOWN)
    if board[i][j] == CellType.RIGHT or (i < N_W_CELLS - 1 and board[i + 1][j] == CellType.LEFT):
        lst.remove(Border.RIGHT)
    if board[i][j] == CellType.LEFT or (i > 0 and board[i - 1][j] == CellType.RIGHT):
        lst.remove(Border.LEFT)
    return lst


def draw_cell(cell, i, j):
    if cell == CellType.SPAWN:
        print_rect(canvas, i, j, "#0AF")

    if cell == CellType.END:
        print_rect(canvas, i, j, "#FF0")
        return

    if cell == CellType.BOSS:
        canvas.create_oval((i + .3) * W_CELL, (j + .3) * H_CELL, (i + .7) * W_CELL, (j + .7) * H_CELL, fill="#00F",
                           outline="#0AF", width=3)
        canvas.create_oval((i + .3) * W_CELL, (j + .3) * H_CELL, (i + .5) * W_CELL, (j + .5) * H_CELL, fill="white")
        return

    borders = get_borders(i, j)

    if Border.UP in borders:
        canvas.create_line(i * W_CELL, j * H_CELL, (i + 1) * W_CELL, j * H_CELL, fill="black")

    if Border.DOWN in borders:
        canvas.create_line(i * W_CELL, (j + 1) * H_CELL, (i + 1) * W_CELL, (j + 1) * H_CELL, fill="black")

    if Border.RIGHT in borders:
        canvas.create_line((i+1) * W_CELL, j * H_CELL, (i + 1) * W_CELL, (j+1) * H_CELL, fill="black")

    if Border.LEFT in borders:
        canvas.create_line(i * W_CELL, (j) * H_CELL, i * W_CELL, (j + 1) * H_CELL, fill="black")

    # canvas.create_rectangle((i + .45) * W_CELL, (j + .45) * H_CELL, (i + .55) * W_CELL, (j + .55) * H_CELL, fill="red")


def print_rect(cnv, i, j, color="black"):
    cnv.create_rectangle(i * W_CELL, j * H_CELL, (i + 1) * W_CELL, (j + 1) * H_CELL, fill=color, outline="red")


def print_matrix():
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="white")

    for i in range(N_W_CELLS):
        x = i * W_CELL
        #canvas.create_line(x, 0, x, HEIGHT, fill="#DDD", width=2)

    for j in range(N_H_CELLS):
        y = j * H_CELL
        #canvas.create_line(0, y, WIDTH, y, fill="#DDD", width=2)

    for i in range(N_W_CELLS):
        for j in range(N_H_CELLS):
            draw_cell(board[i][j], i, j)


def has_boss_neighbour(i, j):
    if i < N_W_CELLS - 1 and board[i + 1][j] == CellType.BOSS:  # check right cell
        return True
    if i > 0 and board[i - 1][j] == CellType.BOSS:  # check left cell
        return True
    if j > 0 and board[i][j - 1] == CellType.BOSS:  # check upper cell
        return True
    if j < N_H_CELLS - 1 and board[i][j + 1] == CellType.BOSS:  # check lower cell
        return True
    return False


def spawn_boss_rooms():
    spawned = 0
    while spawned < N_BOSS_ROOMS:
        i = random.randint(0, N_W_CELLS - 1)
        j = random.randint(0, N_H_CELLS - 1)
        if board[i][j] is None and not has_boss_neighbour(i, j):
            board[i][j] = CellType.BOSS
            spawned += 1


def init_board(spawn_i, spawn_j):
    lst = []
    for i in range(N_W_CELLS):
        for j in range(N_W_CELLS):
            if i == spawn_i and j == spawn_j:
                lst.append(CellType.SPAWN)
            else:
                lst.append(None)
        board.append(lst)
        lst = []
    board[spawn_i][spawn_j] = CellType.SPAWN
    spawn_boss_rooms()


def get_available_neighbours(i, j):
    directions = []
    if i + 1 < N_W_CELLS and board[i + 1][j] is None:
        directions.append(AvailableNeighbours.RIGHT)
    if i > 0 and board[i - 1][j] is None:
        directions.append(AvailableNeighbours.LEFT)
    if j + 1 < N_H_CELLS and board[i][j + 1] is None:
        directions.append(AvailableNeighbours.DOWN)
    if j > 0 and board[i][j - 1] is None:
        directions.append(AvailableNeighbours.UP)
    return directions


def gen_cell(i, j):
    neighbours = get_available_neighbours(i, j)
    while len(neighbours) > 0:
        new_i = i
        new_j = j
        random_neighbour = random.choice(neighbours)
        if random_neighbour == AvailableNeighbours.RIGHT:
            new_i = i + 1
            cell_type = CellType.LEFT
        else:
            if random_neighbour == AvailableNeighbours.LEFT:
                new_i = i - 1
                cell_type = CellType.RIGHT
            else:
                if random_neighbour == AvailableNeighbours.DOWN:
                    new_j = j + 1
                    cell_type = CellType.UP
                else:
                    new_j = j - 1
                    cell_type = CellType.DOWN
        board[new_i][new_j] = cell_type
        gen_cell(new_i, new_j)
        neighbours = get_available_neighbours(i, j)



win = tkinter.Tk()
canvas = tkinter.Canvas(win, bg="white", width=WIDTH, height=HEIGHT)
win.resizable(False, False)

spawn_i = random.randint(0, N_W_CELLS - 1)
spawn_j = random.randint(0, N_H_CELLS - 1)
board = []
init_board(spawn_i, spawn_j)
gen_cell(spawn_i, spawn_j)
print_matrix()

print("End of generation")
seed_str = "SEED:" + str(SEED)
win.title("Maze generation by Marco Sartori " + seed_str)
canvas.pack()
win.mainloop()
