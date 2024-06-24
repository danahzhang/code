import fifteengame2 as game
import random

def test_search_path_1():
    board = game.Puzzle(4,4,1)
    print(board)
    frozen = [(2,1),(1,2)]
    n=1
    current = board.get_current_position(n)
    final = board.get_final_position(n)
    print(current,final)
    path = game.search_path([([], current)], board, final, frozen, [], game.DIRECTIONS)
    assert path == ['d','l','l','u','u','u']

def test_search_path_long_path():
    board = game.Puzzle(4,4,1)
    print(board)
    frozen = [(1,0),(2,1),(1,2)]
    n=3
    print(board)
    current = board.get_current_position(n)
    final = board.get_final_position(n)
    path = game.search_path([([], current)], board, final, frozen, [], game.DIRECTIONS)
    assert path == ['r', 'u', 'r', 'u', 'u', 'l']

def test_search_path_not_to_final():
    board = game.Puzzle(4,4,1)
    print(board)
    frozen = [(1,0),(1,1),(1,2)]
    n=1
    print(board)
    current = board.get_current_position(n)
    final = (0,1)
    path = game.search_path([([], current)], board, final, frozen, [], game.DIRECTIONS)
    assert path == ['r', 'u', 'u', 'l', 'l']

def test_search_path_zero():
    board = game.Puzzle(4,4,1)
    print(board)
    frozen = []
    n=0
    print(board)
    current = board.get_current_position(n)
    final = (1,0)
    path = game.search_path([([], current)], board, final, frozen, [], game.ZERO_DIRECTIONS)
    assert path == ['d', 'r', 'r', 'r']

def test_search_path_zero2():
    board = game.Puzzle(4,4,1)
    print(board)
    frozen = [(1,1)]
    n=0
    print(board)
    current = board.get_current_position(n)
    final = (1,0)
    path = game.search_path([([], current)], board, final, frozen, [], game.ZERO_DIRECTIONS)
    assert path == ['r', 'r', 'r', 'd']

def test_move_one_up():
    board = game.Puzzle(4,4,1)
    print(board)
    path = game.move_number(1,(1,2),board,[])
    assert path == "dru"
    path += game.move_number(1,(0,2),board,[(1,2)])
    assert path == "drulddru"

def test_move_numbers_first_row():
    board = game.Puzzle(4,4,1)
    print(board)
    game.move_number(1,board.get_final_position(1),board,[])
    game.move_number(2,board.get_final_position(2),board,[(0,0)])
    game.move_two_numbers(board.get_final_position(3),board,[(0,0),(0,1)])
    for n in range(1,5):
        assert board.get_current_position(n) == board.get_final_position(n)

def test_solve_rows():
    board = game.Puzzle(4,4,1)
    print(board)
    frozen = []
    path = game.solve_row(0,2, board, frozen)
    path += game.solve_row(1,2, board, frozen)
    for n in range(1, 9):
        assert board.get_current_position(n) == board.get_final_position(n)

def test_solve():
    board = game.Puzzle(4,4,1)
    print(board)
    path = game.solve(board)
    print(path) 
    board2 = game.Puzzle(4,4,1)
    board2.use_solution(path)
    assert board.get_grid() == board2.get_grid()
    for n in range(1, 16):
        assert board.get_current_position(n) == board.get_final_position(n)
    
def test_solve_3_by_3():
    pass


