import fifteengame2 as game
import random

def test_search_path_1():
    board = create_test_board()
    frozen = [(2,1),(2,2)]
    n=1
    print(board)
    current = board.get_current_position(n)
    final = board.get_final_position(n)
    path = game.search_path([([], current)], board, final, frozen, [], game.DIRECTIONS)
    assert path == ['l', 'u', 'u', 'u']

def test_search_path_long_path():
    board = create_test_board()
    frozen = [(0,1), (2,1), (1,2),(2,2)]
    n=3
    print(board)
    current = board.get_current_position(n)
    final = board.get_final_position(n)
    path = game.search_path([([], current)], board, final, frozen, [], game.DIRECTIONS)
    assert path == ['l', 'd', 'd', 'r', 'r', 'r', 'u', 'u', 'u', 'l']

def test_search_path_not_to_final():
    board = create_test_board()
    frozen = [(1,1),(1,2)]
    n=4
    print(board)
    current = board.get_current_position(n)
    final = (0,1)
    path = game.search_path([([], current)], board, final, frozen, [], game.DIRECTIONS)
    assert path == ['u', 'r', 'u', 'u', 'l', 'l']

def test_search_path_zero():
    board = create_test_board()
    frozen = []
    n=0
    print(board)
    current = board.get_current_position(n)
    final = (1,0)
    path = game.search_path([([], current)], board, final, frozen, [], game.ZERO_DIRECTIONS)
    assert path == ['r', 'r']

def test_search_path_zero2():
    board = create_test_board()
    frozen = [(1,1)]
    n=0
    print(board)
    current = board.get_current_position(n)
    final = (1,0)
    path = game.search_path([([], current)], board, final, frozen, [], game.ZERO_DIRECTIONS)
    assert path == ['d', 'r', 'r', 'u']

def test_move_one_up():
    board = create_test_board()
    path = game.move_number(1,(2,1),board,[])
    assert path == "uru"
    path += game.move_number(1,(1,1),board,[(2,1)])
    assert path == "urulddru"

def test_move_numbers_first_row():
    board = create_test_board()
    game.move_number(1,board.get_final_position(1),board,[])
    game.move_number(2,board.get_final_position(2),board,[(0,0)])
    game.move_two_numbers(board.get_final_position(3),board,[(0,0),(0,1)])
    for n in range(1,5):
        assert board.get_current_position(n) == board.get_final_position(n)

def test_solve_rows():
    board = create_test_board()
    frozen = []
    path = game.solve_row(0,2, board, frozen)
    path += game.solve_row(1,2, board, frozen)
    for n in range(1, 9):
        assert board.get_current_position(n) == board.get_final_position(n)

def test_solve():
    board = create_test_board()
    path = game.solve(board)
    print(path) 
    board2 = create_test_board()
    board2.use_solution(path)
    assert board.get_grid() == board2.get_grid()
    for n in range(1, 16):
        assert board.get_current_position(n) == board.get_final_position(n)
    
def create_test_board():
    l = list(range(0,16))
    random.Random(4).shuffle(l)
    grid =[]
    for i in range(0,16,4):
        grid.append([l[i+n] for n in range(0,4)])
    return game.Puzzle(4, 4, grid)
