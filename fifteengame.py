import random
DIRECTIONS = {
    "l": {"name":"l","index":(0, 1),"opposite":"r","name":"left"},
    "r": {"name":"r","index":(0, -1),"opposite":"l","name":"right"},
    "u": {"name":"u","index":(1, 0),"opposite":"d","name":"up"},
    "d": {"name":"d","index":(-1, 0),"opposite":"u","name":"down"}
}
    
class Puzzle():
    
    def __init__(self, row=3, col=3, grid = []):
        if not grid:
            self._row = row
            self._col = col
        else:
            self._row = len(grid)
            self._col = len(grid[0])
        
        numbers = list(range(1, self._row*self._col))+ [0]
        index = 0
        self._finished_grid = []
        for dummyrow in range(row):
            column = []
            for dummycol in range(col):
                column.append(numbers[index])
                index += 1
            self._finished_grid.append(column)
        
        if not grid:
            random.shuffle(numbers)
            self._grid = [[numbers.pop() for dummycol in range(col)] for dummyrow in range(row)]

        else:
            flatten_grid = []
            for row in range(self._row):
                assert len(grid[row]) == self._row, "inputted rows aren't meeting length"
                flatten_grid += grid[row] 
                
            assert len(set(flatten_grid)) == len(flatten_grid), "numbers in inputted grid not unique"
            assert max(flatten_grid) == self._row * self._col - 1, "max should be " + self._row * self._col - 1 + "but is " + max(flatten_grid)
            assert min(flatten_grid) == 0, "max should be zero but is " + min(flatten_grid) 
            self._grid = grid

            
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

    def get_row(self):
        return self._row
    
    def get_col(self):
        return self._col
    
    def get_grid(self):
        return self._grid
    
    def get_finished_grid(self):
        return self._finished_grid
    
    def get_position(self, number):
        for row in range(self._row):
            for col in range(self._col):
                a_number = self._grid[row][col]
                if a_number == number:
                    return (row, col)


    def get_number(self, row, col):
        return self._grid[row][col]

    def get_correct_number(self, row, col):
        return self._finished_grid[row][col]
    
    def make_clone(self):
        clone = Puzzle(self._row, self._col)
        for row in range(self._row):
            for col in range(self._col):
                clone._grid[row][col] = self._grid[row][col]
        return clone

    def find_zero(self):
        return self.get_position(0)

    def find_nonempty_square(self, arrow):
        row_change, col_change = DIRECTIONS[arrow]["index"]
        row, col = self.find_zero()
        row += row_change 
        col += col_change
        assert row < self._row and row >= 0 and col < self._col and col >= 0, "can't move " + DIRECTIONS[arrow]["name"]
        return (row, col)
    
    def find_number(self, number):
        assert self._row * self._col > number >= 0, "number too big or too small"
        for row in range(self._row):
            for col in range(self._col):
                if self._grid[row][col] == number:
                    return (row, col)

    def check_value(self, row, col):
        return self._finished_grid[row][col] == self.get_number(row, col)

    def move(self, arrow):
        row_one, col_one = self.find_zero()
        new_square = self.find_nonempty_square(arrow)
        if new_square:
            row_two, col_two = new_square
            self._grid[row_one][col_one], self._grid[row_two][col_two] = self._grid[row_two][col_two], self._grid[row_one][col_one]
          
    def use_solution(self, pattern):
        for letter in pattern:
            self.move(letter)
            print(self)

board = Puzzle(3, 3, [[1,2,3],[4,5,6],[7,8,0]])
board.use_solution("rddrul")

def basic_freeze(direction, board, number, temp = None):
    empty_row, empty_col = board.find_zero()
    direction_row
    empty_row, empty_col = empty_row + direction["index"][0], empty_col + direction["index"][1]
    if empty_row < 0 or empty_row >= board.get_row() or empty_col < 0 or empty_col >= board.get_col():
        return False
    new_empty = (empty_row, empty_col)
    if number > 1:
        for num in range(1,number):
            if board.get_position(num) == new_empty:
                return False
    if temp and temp == new_empty:
        return False
    return True

boards = [(board,[None],basic_freeze)]

def search_path(number, final_position, freeze):
    board, move_list, temp = boards.pop(0)
    if board.find_number(number) == final_position:
        return move_list
    for direction in DIRECTIONS:
        if (not move_list[-1] or DIRECTIONS[move_list[-1]]["opposite"] != direction) and freeze(direction, board, number, temp):
            boards.append((board.make_clone().move(direction["name"]), move_list + [direction["name"]], temp))
    search_path(number, final_position, freeze)

print(search_path(1, (0,0), basic_freeze))




def test_case(row, col):
    trial = Puzzle(row, col) 
    print("The Puzzle")
    print(trial)

    rows = trial.get_row()
    cols = trial.get_col()
    grid = trial.get_grid()
    assert cols == len(grid), "grid's number of columns doesn;t match dim"
    assert rows == len(grid[0]), "grid's number of rows doesn't match dim"
    
    max_num = cols*rows
    for row in range(rows):
        for col in range(cols):
            assert grid[row][col] < max_num, "grids' number too large"

    empty_row, empty_col = trial.find_zero()
    assert grid[empty_row][empty_col] == 0, "find_empty_square() returns nonempty square"
    
    trial_clone = trial.make_clone()
    assert trial_clone.get_grid() == grid, "get_clone() doesn't make a clone"

    number = random.randrange(1, rows*cols)

    number_location = trial.find_number(number)
    assert number == grid[number_location[0]][number_location[1]]

#test_case(4,4)
