board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

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

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("------------------------------------")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end=" ")    # Remain on same line for next iteration
            if j == 8:                      # If 8, just print it, got to next line for next iteration
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end=" ")    # Remain on same line for next iteration

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)               # Row,Col
    return None

