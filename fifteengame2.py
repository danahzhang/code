import random
DIRECTIONS = {
    "u": (-1, 0),
    "d": (1, 0),
    "r": (0, 1),
    "l": (0, -1)
}

ZERO_DIRECTIONS = {
    "d": (-1, 0),
    "u": (1, 0),
    "l": (0, 1),
    "r": (0, -1)
}
    
class Puzzle():
    
    def __init__(self, row=3, col=3, seed = None, grid = []):
        self._row = row
        self._col = col
        numbers = list(range(1, self._row*self._col))+ [0]
        index = 0
        self._grid = []
        self._finished_grid = []
        for dummyrow in range(row):
            column = []
            finished_column = []
            for dummycol in range(col):
                column.append(numbers[index])
                finished_column.append(numbers[index])
                index += 1
            self._grid.append(column)
            self._finished_grid.append(finished_column)
        self.shuffle(seed)

    def __str__(self):
        s = ""
        for row in range(self._row):
            for col in range(self._col):
                number = self._grid[row][col]
                s += "  "
                if number < 10:
                    s += " "
                if number == 0:
                    number = " "
                s += str(number) 
            s += '\n'
        return s

    def get_rows(self):
        return self._row
    
    def get_cols(self):
        return self._col
    
    def get_grid(self):
        return self._grid
    
    def get_position(self, grid, number):
        for row in range(self._row):
            for col in range(self._col):
                a_number = grid[row][col]
                if a_number == number:
                    return (row, col)

    def get_current_position(self, number):
        return self.get_position(self._grid, number)
    
    def get_final_position(self, number):
        return self.get_position(self._finished_grid, number)
    
    def get_zero(self):
        return self.get_current_position(0)

    def get_nonzero(self, arrow):
        row_change, col_change = ZERO_DIRECTIONS[arrow]
        row, col = self.get_zero()
        row += row_change 
        col += col_change
        assert row < self._row and row >= 0 and col < self._col and col >= 0, "can't move " + arrow
        return (row, col)

    def check_correct_value(self, row, col):
        return self._finished_grid[row][col]

    def move(self, arrow, printing=True):
        row_one, col_one = self.get_zero()
        new_square = self.get_nonzero(arrow)
        if new_square:
            row_two, col_two = new_square
            self._grid[row_one][col_one], self._grid[row_two][col_two] = self._grid[row_two][col_two], self._grid[row_one][col_one]
            if printing:
                print(self)

    def use_solution(self, pattern):
        for letter in pattern:
            self.move(letter)
            print(self)
    
    def shuffle(self, seed=None):
        current_row, current_col = self.get_zero()
        sequence = [arrow for dummynum in range(self._col*self._row*2) for arrow in ['l',"r","u","d"]]
        random.Random(seed).shuffle(sequence)
        for arrow in sequence:
            row, col = ZERO_DIRECTIONS[arrow]
            if self.check_in(current_row+row, current_col+col):
                self.move(arrow, False)
                current_row, current_col = self.get_zero()

    def check_in(self, row, col):
        if row >= self._row or row < 0 or col >= self._col or col < 0:
            return False
        return True
  
def search_path(paths, board, final, frozen, visited, directions):
    path, current = paths.pop(0)
    if current == final:
        return path
    for direction, value in directions.items():
        new_current = (current[0]+value[0], current[1]+value[1])
        if board.check_in(new_current[0], new_current[1]) and new_current not in frozen and new_current not in visited:
            paths.append((path+[direction], new_current))
            visited.append(new_current)
    return search_path(paths, board, final, frozen, visited, directions)

def move_number(number, position, board, frozen):
    path = ""
    current_position = board.get_current_position(number)
    number_path = search_path([([], current_position)], board, position, frozen, [], DIRECTIONS)
    for arrow in number_path:
        next_position = (current_position[0]+DIRECTIONS[arrow][0], current_position[1]+DIRECTIONS[arrow][1])
        path += move_zero(next_position,board,frozen,temp=current_position)
        path += arrow
        board.move(arrow)
        current_position = next_position
    return path

def move_zero(position, board, frozen, temp=None):
    path = ""
    zero_position = board.get_zero()
    zero_path = search_path([([], zero_position)], board, position, frozen, [temp], ZERO_DIRECTIONS)
    for arrow in zero_path:
        path += arrow
        board.move(arrow)
    return path

def move_two_numbers(position_one, board, frozen):
    path = ""
    position_two, position_temp, position_backup = find_six_grid(position_one)
    number_one = board.check_correct_value(position_one[0],position_one[1])
    number_two = board.check_correct_value(position_two[0],position_two[1])
    if board.get_current_position(number_two) == position_two:
      path += move_number(number_two, position_backup, board, frozen)
    path += move_number(number_one, position_two, board, frozen)
    print(frozen)
    path += move_number(number_two, position_temp, board, frozen+[position_two])
    path += move_number(number_one, position_one, board, frozen[:-1]+[position_temp])
    path += move_number(number_two, position_two, board, frozen[:-1]+[position_one])
    frozen.append(position_one)
    frozen.append(position_two)
    return path

def solve_row(row, col, board, frozen):
    path = ""
    for col in range(col):
        position = (row, col)
        number = board.check_correct_value(row, col)
        path += move_number(number, position, board, frozen)
        frozen.append(position)
    path += move_two_numbers((row, col+1), board, frozen)
    return path

def find_six_grid(position):
    row, col = position
    if col == 2:
        return (row, col+1), (row+1, col+1), (row+2, col+1)
    elif row == 3:
        return (row-1, col), (row-1, col+1), (row-1, col+2)
    
def solve(board):
    rows, cols = board.get_rows(), board.get_cols()
    path = ""
    frozen = []
    for row in range(rows-2):
        path += solve_row(row, cols-2, board, frozen)
    for col in range(cols-2):
        position = (rows-1, col)
        path += move_two_numbers(position, board, frozen)
    final_number = board.get_rows()*board.get_cols()-1
    final_position = board.get_final_position(final_number)
    path += move_number(final_number, final_position, board, frozen)
    path += move_zero(board.get_final_position(0), board, frozen+[final_position])
    return path
