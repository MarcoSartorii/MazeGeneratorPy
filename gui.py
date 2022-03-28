import random
import tkinter
from enum import Enum

SEED = random.randint(0, 1000)
random.seed(SEED)

WIDTH = 675
HEIGHT = 675
N_W_CELLS = 15
N_H_CELLS = 15
N_BOSS_ROOMS = 10
W_CELL = WIDTH / N_W_CELLS
H_CELL = HEIGHT / N_H_CELLS

MAX_ROOMS_BOUND = 4
UPPER_DOOR_COLOR = "red"
LOWER_DOOR_COLOR = "lime"
RIGHT_DOOR_COLOR = "blue"
LEFT_DOOR_COLOR = "magenta"
MARGIN_DOOR_PIXELS = 7


class AvailableNeighbours(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class CellType(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    SPAWN = 4
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
        canvas.create_line((i + 1) * W_CELL, j * H_CELL, (i + 1) * W_CELL, (j + 1) * H_CELL, fill="black")

    if Border.LEFT in borders:
        canvas.create_line(i * W_CELL, j * H_CELL, i * W_CELL, (j + 1) * H_CELL, fill="black")

    if board[i][j] is None:
        canvas.create_rectangle((i + .45) * W_CELL, (j + .45) * H_CELL, (i + .55) * W_CELL, (j + .55) * H_CELL,
                                fill="red")


def print_rect(cnv, i, j, color="black"):
    cnv.create_rectangle(i * W_CELL, j * H_CELL, (i + 1) * W_CELL, (j + 1) * H_CELL, fill=color, outline="red")


def print_matrix():
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="white")

    """
    -------------------------------
    uncomment to draw the gray grid
    -------------------------------
    """
    """ 
    for i in range(N_W_CELLS):
        x = i * W_CELL
        canvas.create_line(x, 0, x, HEIGHT, fill="#DDD", width=2)

    for j in range(N_H_CELLS):
        y = j * H_CELL
        canvas.create_line(0, y, WIDTH, y, fill="#DDD", width=2)
    """

    for i in range(N_W_CELLS):
        for j in range(N_H_CELLS):
            draw_cell(board[i][j], i, j)
    for (i, j) in doors:
        if board[i][j] == CellType.UP:
            canvas.create_line(i * W_CELL + 1 + MARGIN_DOOR_PIXELS, j * H_CELL,
                               (i + 1) * W_CELL - 1 - MARGIN_DOOR_PIXELS, j * H_CELL, fill=UPPER_DOOR_COLOR,
                               width=3)
        else:
            if board[i][j] == CellType.DOWN:
                canvas.create_line(i * W_CELL + 1 + MARGIN_DOOR_PIXELS, (j + 1) * H_CELL,
                                   (i + 1) * W_CELL - 1 - MARGIN_DOOR_PIXELS, (j + 1) * H_CELL,
                                   fill=LOWER_DOOR_COLOR, width=3)
            else:
                if board[i][j] == CellType.RIGHT:
                    canvas.create_line((i + 1) * W_CELL, j * H_CELL + 1 + MARGIN_DOOR_PIXELS, (i + 1) * W_CELL,
                                       (j + 1) * H_CELL - 1 - MARGIN_DOOR_PIXELS,
                                       fill=RIGHT_DOOR_COLOR, width=3)
                else:
                    canvas.create_line(i * W_CELL, j * H_CELL + 1 + MARGIN_DOOR_PIXELS, i * W_CELL,
                                       (j + 1) * H_CELL - 1 - MARGIN_DOOR_PIXELS,
                                       fill=LEFT_DOOR_COLOR, width=3)


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


def has_too_much_boss_neighbours(i, j):
    if i == 0 and j == 0:  # TOP_LEFT corner
        if board[i + 1][j] == CellType.BOSS and board[i][j + 1] == CellType.BOSS:
            return True
    if i == 0 and j == N_H_CELLS - 1:  # BOTTOM_LEFT corner
        if board[i + 1][j] == CellType.BOSS and board[i][j - 1] == CellType.BOSS:
            return True
    if i == N_W_CELLS - 1 and j == 0:  # TOP_RIGHT corner
        if board[i - 1][j] == CellType.BOSS and board[i][j + 1] == CellType.BOSS:
            return True
    if i == N_W_CELLS - 1 and j == N_H_CELLS - 1:  # BOTTOM_RIGHT corner
        if board[i - 1][j] == CellType.BOSS and board[i][j - 1] == CellType.BOSS:
            return True
    """
    lst = []
    lst.append(board[i + 1][j])
    lst.append(board[i - 1][j])
    lst.append(board[i][j + 1])
    lst.append(board[i][j - 1])
    print(lst)  
    tired of fixing the boss logic spawn, Imma do it tomorrow
    """
    return False


def spawn_boss_rooms():
    spawned = 0
    while spawned < N_BOSS_ROOMS:
        i = random.randint(1, N_W_CELLS - 2)
        j = random.randint(1, N_H_CELLS - 2)
        if board[i][j] is None and not has_boss_neighbour(i, j):
            board[i][j] = CellType.BOSS
            boss_doors.append((i, j, random.choice([Border.LEFT, Border.RIGHT, Border.DOWN, Border.UP])))
            spawned += 1
        for k in range(N_W_CELLS):
            for h in range(N_H_CELLS):
                if has_too_much_boss_neighbours(h, k):
                    board[i][j] = None
    print(boss_doors)


def init_board(spawn_i_, spawn_j_):
    lst = []
    for i in range(N_W_CELLS):
        for j in range(N_W_CELLS):
            if i == spawn_i_ and j == spawn_j_:
                lst.append(CellType.SPAWN)
            else:
                lst.append(None)
        board.append(lst)
        lst = []
    board[spawn_i_][spawn_j_] = CellType.SPAWN
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
    sons = []

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
        cells = gen_cell(new_i, new_j)
        sons.append((new_i, new_j, cells))
        neighbours = get_available_neighbours(i, j)

    sons.sort(key=lambda x: x[2])

    if len(sons) == 3:
        s = sons[0][2] + sons[1][2] + sons[2][2] + 1
        if s < MAX_ROOMS_BOUND:
            return s
        if s == MAX_ROOMS_BOUND:
            doors.append((i, j))
            return 0
        doors.append((sons[2][0], sons[2][1]))

    if len(sons) >= 2:
        s = sons[0][2] + sons[1][2] + 1
        if s < MAX_ROOMS_BOUND:
            return s
        if s == MAX_ROOMS_BOUND:
            doors.append((i, j))
            return 0
        doors.append((sons[1][0], sons[1][1]))

    if len(sons) >= 1:
        s = sons[0][2] + 1
        if s < MAX_ROOMS_BOUND:
            return s
        if s == MAX_ROOMS_BOUND:
            doors.append((i, j))
            return 0
        doors.append((sons[0][0], sons[0][1]))

    return 1


win = tkinter.Tk()
canvas = tkinter.Canvas(win, bg="white", width=WIDTH, height=HEIGHT)
win.resizable(False, False)

spawn_i = random.randint(0, N_W_CELLS - 1)
spawn_j = random.randint(0, N_H_CELLS - 1)
doors = []
boss_doors = []
board = []
init_board(spawn_i, spawn_j)
gen_cell(spawn_i, spawn_j)
print_matrix()

print("End of generation")
seed_str = "SEED:" + str(SEED)
win.title("Maze generation by Marco Sartori with a little help from KelpsEater: " + seed_str)
canvas.pack()
win.mainloop()
