import pygame
import time

pygame.init()

global black, white
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
grey = (128, 128, 128)
red = (255, 0, 0)

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)               # Row,Col
    return None

def valid(bo, num, pos):          # num - Number we just entered, pos - Tuple (Row, Col)

    for i in range(len(bo[0])):             # Check Row
        if bo[pos[0]][i] == num and i != pos[1]:
            return False

    for j in range(len(bo)):                # Check Column
        if bo[j][pos[1]] == num and j != pos[0]:
            return False

    box_x = pos[0] // 3                     # Boxes will be -->> (0,0),(0,1)...(2,2)
    box_y = pos[1] // 3                     # Returns either 0, 1 or 2
    # To find the element inside the box
    for i in range(box_x * 3, box_x * 3 + 3):       # box_x/y * 3 -->> To find first element in that box
        for j in range(box_y * 3, box_y * 3 + 3):       # + 3 to check the next 3 elements
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def solve(bo):
    find = find_empty(bo)           # Find an empty cell
    if not find:
        return True                 # Board is full
    else:
        (row,col) = find            # Position to check

    for i in range(1,10):
        if valid(bo, i, (row,col)):     # If it's valid with i
            bo[row][col] = i            # Place i in that cell

            if solve(bo):               # Recursion
                return bo

            bo[row][col] = 0            # If solve returned False, make it back to 0

    return False

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.win = win
        self.selected = None
        self.model = None
        self.finished = None

    def draw_grid(self):
        blocksize = self.width//9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 2
            pygame.draw.line(self.win, black, (0, i*blocksize), (self.width, i*blocksize), thick)
            pygame.draw.line(self.win, black, (i*blocksize, 0), (i*blocksize, self.height), thick)
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

        if self.finished:
            fnt = pygame.font.SysFont('comicsans', 80)
            text = fnt.render("GAME OVER", 1, red)
            self.win.blit(text, (self.width//2 - text.get_width()//2, (self.height - 60)//2 - text.get_height()//2))

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            blocksize = self.width//9
            x = pos[0]//blocksize
            y = pos[1]//blocksize
            return (int(x), int(y))
        return None

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, value):
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.board):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    self.finished = False
                    return False
        self.finished = True

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False

    def draw(self, win):
        blocksize = self.width//9
        x = self.row * blocksize
        y = self.col * blocksize

        fnt = pygame.font.SysFont('comicsans', 40)

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, grey)
            win.blit(text, (x+5, y+5))
        elif self.value != 0:
            text = fnt.render(str(self.value), 1 , black)
            win.blit(text, (x + blocksize//2 - text.get_width()//2, y + blocksize//2 - text.get_height()//2))

        if self.selected:
            pygame.draw.rect(win, red, (x, y, blocksize, blocksize), 3)

    def draw_change(self, win, g = True):
        blocksize = self.width//9
        x = self.row * blocksize
        y = self.col * blocksize

        fnt = pygame.font.SysFont('comicsans', 40)

        pygame.draw.rect(win, white, (x, y, blocksize, blocksize), 0)

        text = fnt.render(str(self.value), 1, black)
        win.blit(text, (x + (blocksize//2 - text.get_width()//2), y + (blocksize//2 - text.get_height()//2)))

        if g:
            pygame.draw.rect(win, green, (x, y, blocksize, blocksize), 3)
        else:
            pygame.draw.rect(win, red, (x, y, blocksize, blocksize), 3)

    def set_temp(self, val):
        self.temp = val

    def set(self, val):
        self.value = val

def redraw_grid(win, board, time, strikes):
    win.fill(white)
    fnt = pygame.font.SysFont('comicsans', 40)
    text = fnt.render("Time: " + format_time(time), 1, black)
    win.blit(text, (540-160, 560))
    text = fnt.render("X " * strikes, 1, red)
    win.blit(text, (20, 560))
    board.draw_grid()

def format_time(secs):
    sec = secs % 60
    minute = secs//60
    hour = minute//60
    final = " " + str(minute) + ": " + str(sec)
    return final


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    start = time.time()
    strikes = 0
    key = None
    run = True

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = board.click(position)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if not board.place(board.cubes[i][j].temp):
                            strikes += 1
                        key = None

                    board.is_finished()

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

        if board.selected and key != None:
            board.sketch(key)

        redraw_grid(win, board, play_time, strikes)
        pygame.display.update()

main()
