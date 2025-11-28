"""
Unit tests for Puzzle class in model.py.

Tests core puzzle functionality including initialization, moves,
win condition checking, hashing, and simulation.
"""

import sys
import os

import model
from model import Puzzle, WINNING_BOARDS


# Initialization tests

def test_init_3x3():
    """Puzzle initializes to solved state for 3x3."""
    puzzle = Puzzle(boardSize=3)
    assert puzzle.boardSize == 3
    assert puzzle.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    assert puzzle.blank_position == (2, 2)


def test_init_4x4():
    """Puzzle initializes to solved state for 4x4."""
    puzzle = Puzzle(boardSize=4)
    assert puzzle.boardSize == 4
    assert puzzle.board == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    assert puzzle.blank_position == (3, 3)


def test_init_5x5():
    """Puzzle initializes to solved state for 5x5."""
    puzzle = Puzzle(boardSize=5)
    assert puzzle.boardSize == 5
    assert puzzle.blank_position == (4, 4)
    assert puzzle.board[0] == [1, 2, 3, 4, 5]
    assert puzzle.board[4][4] == 0


def test_init_default_size():
    """Puzzle defaults to 4x4 when no size specified."""
    puzzle = Puzzle()
    assert puzzle.boardSize == 4


# Move tests

def test_move_up_valid():
    """Moving up from middle position works."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
    puzzle.blank_position = (1, 2)

    result = puzzle.move(Puzzle.UP)

    assert result is True
    assert puzzle.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    assert puzzle.blank_position == (2, 2)


def test_move_down_valid():
    """Moving down from middle position works."""
    puzzle = Puzzle(boardSize=3)

    result = puzzle.move(Puzzle.DOWN)

    assert result is True
    assert puzzle.board == [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
    assert puzzle.blank_position == (1, 2)


def test_move_left_valid():
    """Moving left from middle position works."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    puzzle.blank_position = (2, 1)

    result = puzzle.move(Puzzle.LEFT)

    assert result is True
    assert puzzle.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    assert puzzle.blank_position == (2, 2)


def test_move_right_valid():
    """Moving right from middle position works."""
    puzzle = Puzzle(boardSize=3)

    result = puzzle.move(Puzzle.RIGHT)

    assert result is True
    assert puzzle.board == [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    assert puzzle.blank_position == (2, 1)


def test_move_up_from_bottom_invalid():
    """Cannot move UP when blank at bottom (UP moves blank down)."""
    puzzle = Puzzle(boardSize=3)
    # Blank at bottom-right (2,2), UP would move it to (3,2) - invalid

    result = puzzle.move(Puzzle.UP)

    assert result is False
    assert puzzle.blank_position == (2, 2)


def test_move_down_from_top_invalid():
    """Cannot move DOWN when blank at top (DOWN moves blank up)."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    puzzle.blank_position = (0, 0)

    result = puzzle.move(Puzzle.DOWN)

    assert result is False
    assert puzzle.blank_position == (0, 0)


def test_move_left_from_right_edge_invalid():
    """Cannot move LEFT when blank at right edge (LEFT moves blank right)."""
    puzzle = Puzzle(boardSize=3)
    # Blank at bottom-right (2,2), LEFT would move it to (2,3) - invalid

    result = puzzle.move(Puzzle.LEFT)

    assert result is False
    assert puzzle.blank_position == (2, 2)


def test_move_right_from_left_edge_invalid():
    """Cannot move RIGHT when blank at left edge (RIGHT moves blank left)."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[1, 2, 3], [0, 4, 5], [6, 7, 8]]
    puzzle.blank_position = (1, 0)

    result = puzzle.move(Puzzle.RIGHT)

    assert result is False
    assert puzzle.blank_position == (1, 0)


def test_move_sequence():
    """Series of moves produces expected result."""
    puzzle = Puzzle(boardSize=3)
    # Starting from solved: blank at (2,2)
    # RIGHT moves blank left to (2,1)
    # UP moves blank down to (3,1) - INVALID, so stays at (2,1)
    # Actually UP from (2,1) would try to move to (3,1) which is out of bounds

    puzzle.move(Puzzle.RIGHT)  # blank moves left: (2,2) -> (2,1)
    puzzle.move(Puzzle.UP)      # blank tries to move down: (2,1) -> (3,1) - INVALID

    assert puzzle.board == [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    assert puzzle.blank_position == (2, 1)


# Win condition tests

def test_checkwin_solved_3x3():
    """Solved 3x3 puzzle returns True."""
    puzzle = Puzzle(boardSize=3)
    assert puzzle.checkWin() is True


def test_checkwin_solved_4x4():
    """Solved 4x4 puzzle returns True."""
    puzzle = Puzzle(boardSize=4)
    assert puzzle.checkWin() is True


def test_checkwin_solved_5x5():
    """Solved 5x5 puzzle returns True."""
    puzzle = Puzzle(boardSize=5)
    assert puzzle.checkWin() is True


def test_checkwin_one_move_away_3x3():
    """Puzzle one move from solved returns False."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    puzzle.blank_position = (2, 1)
    assert puzzle.checkWin() is False


def test_checkwin_scrambled_4x4():
    """Scrambled puzzle returns False."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[5, 1, 2, 4], [9, 6, 3, 8], [0, 10, 7, 11], [13, 14, 15, 12]]
    puzzle.blank_position = (2, 0)
    assert puzzle.checkWin() is False


def test_checkwin_uses_predefined_boards():
    """checkWin uses predefined WINNING_BOARDS for common sizes."""
    puzzle = Puzzle(boardSize=4)
    assert puzzle.board == WINNING_BOARDS[4]
    assert puzzle.checkWin() is True


def test_checkwin_after_move():
    """checkWin returns False after making move from solved state."""
    puzzle = Puzzle(boardSize=3)
    puzzle.move(Puzzle.RIGHT)
    assert puzzle.checkWin() is False


# Simulate move tests

def test_simulate_move_valid_doesnt_modify_original():
    """simulateMove doesn't modify original puzzle."""
    puzzle = Puzzle(boardSize=3)
    original_board = [row[:] for row in puzzle.board]
    original_blank = puzzle.blank_position

    is_valid, new_puzzle = puzzle.simulateMove(Puzzle.RIGHT)

    assert is_valid is True
    assert puzzle.board == original_board
    assert puzzle.blank_position == original_blank


def test_simulate_move_valid_returns_new_state():
    """simulateMove returns new puzzle with move applied."""
    puzzle = Puzzle(boardSize=3)

    is_valid, new_puzzle = puzzle.simulateMove(Puzzle.RIGHT)

    assert is_valid is True
    assert new_puzzle.board == [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    assert new_puzzle.blank_position == (2, 1)


def test_simulate_move_invalid():
    """simulateMove returns False for invalid move."""
    puzzle = Puzzle(boardSize=3)
    # Blank at bottom-right (2,2), UP would move it down to (3,2) - invalid

    is_valid, new_puzzle = puzzle.simulateMove(Puzzle.UP)

    assert is_valid is False
    assert puzzle.blank_position == (2, 2)


def test_simulate_move_returns_independent_copy():
    """Modifying simulated puzzle doesn't affect original."""
    puzzle = Puzzle(boardSize=3)
    # Original blank at (2,2)
    # Simulate RIGHT: blank moves left to (2,1)
    # Then move UP on copy: tries to move blank down to (3,1) - INVALID

    is_valid, new_puzzle = puzzle.simulateMove(Puzzle.RIGHT)
    new_puzzle.move(Puzzle.UP)  # Invalid move, blank stays at (2,1)

    assert puzzle.blank_position == (2, 2)
    assert new_puzzle.blank_position == (2, 1)


# Hash tests

def test_hash_full_board():
    """Hash with empty group includes all tiles."""
    puzzle = Puzzle(boardSize=3)
    hash_val = puzzle.hash()

    assert isinstance(hash_val, str)
    assert len(hash_val) > 0


def test_hash_with_group():
    """Hash with specific tile group."""
    puzzle = Puzzle(boardSize=3)
    group = {1, 2, 3}
    hash_val = puzzle.hash(group)

    assert isinstance(hash_val, str)
    assert len(hash_val) < len(puzzle.hash())


def test_hash_different_states_different_hash():
    """Different puzzle states produce different hashes."""
    puzzle1 = Puzzle(boardSize=3)
    puzzle2 = Puzzle(boardSize=3)
    puzzle2.board = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]

    assert puzzle1.hash() != puzzle2.hash()


def test_hash_same_state_same_hash():
    """Same puzzle state produces same hash."""
    puzzle1 = Puzzle(boardSize=3)
    puzzle2 = Puzzle(boardSize=3)

    assert puzzle1.hash() == puzzle2.hash()


def test_hash_deterministic():
    """Hash is deterministic for same state."""
    puzzle = Puzzle(boardSize=3)
    hash1 = puzzle.hash()
    hash2 = puzzle.hash()

    assert hash1 == hash2


# String representation tests

def test_str_representation():
    """String representation contains all tiles."""
    puzzle = Puzzle(boardSize=3)
    str_repr = str(puzzle)

    assert '1' in str_repr
    assert '8' in str_repr
    assert '0' in str_repr
    assert '\n' in str_repr


def test_str_representation_multiline():
    """String representation has correct number of lines."""
    puzzle = Puzzle(boardSize=3)
    str_repr = str(puzzle)
    lines = str_repr.strip().split('\n')

    assert len(lines) == 3


def test_getitem_indexing():
    """Puzzle supports array-like indexing."""
    puzzle = Puzzle(boardSize=3)

    assert puzzle[0][0] == 1
    assert puzzle[2][2] == 0
    assert puzzle[1][1] == 5


def test_getitem_returns_row():
    """Indexing returns entire row."""
    puzzle = Puzzle(boardSize=3)

    assert puzzle[0] == [1, 2, 3]
    assert puzzle[1] == [4, 5, 6]
    assert puzzle[2] == [7, 8, 0]


# Direction constants tests

def test_direction_constants_exist():
    """All direction constants are defined."""
    assert hasattr(Puzzle, 'UP')
    assert hasattr(Puzzle, 'DOWN')
    assert hasattr(Puzzle, 'LEFT')
    assert hasattr(Puzzle, 'RIGHT')
    assert hasattr(Puzzle, 'DIRECTIONS')


def test_directions_list_has_all_directions():
    """DIRECTIONS list contains all four directions."""
    assert len(Puzzle.DIRECTIONS) == 4
    assert Puzzle.UP in Puzzle.DIRECTIONS
    assert Puzzle.DOWN in Puzzle.DIRECTIONS
    assert Puzzle.LEFT in Puzzle.DIRECTIONS
    assert Puzzle.RIGHT in Puzzle.DIRECTIONS


def test_direction_values():
    """Direction constants have correct tuple values."""
    assert Puzzle.UP == (1, 0)
    assert Puzzle.DOWN == (-1, 0)
    assert Puzzle.LEFT == (0, 1)
    assert Puzzle.RIGHT == (0, -1)


# WINNING_BOARDS constant tests

def test_winning_boards_defined():
    """WINNING_BOARDS constant exists."""
    assert WINNING_BOARDS is not None


def test_winning_boards_has_common_sizes():
    """WINNING_BOARDS includes common puzzle sizes."""
    assert 3 in WINNING_BOARDS
    assert 4 in WINNING_BOARDS
    assert 5 in WINNING_BOARDS


def test_winning_board_3x3_correct():
    """3x3 winning board is correct."""
    assert WINNING_BOARDS[3] == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


def test_winning_board_4x4_correct():
    """4x4 winning board is correct."""
    assert WINNING_BOARDS[4] == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


def test_winning_board_5x5_correct():
    """5x5 winning board is correct."""
    expected = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15], [16, 17, 18, 19, 20],
                [21, 22, 23, 24, 0]]
    assert WINNING_BOARDS[5] == expected


# Edge case tests

def test_blank_position_tracks_correctly():
    """Blank position is correctly updated after moves."""
    puzzle = Puzzle(boardSize=3)
    # Start: blank at (2,2)

    puzzle.move(Puzzle.RIGHT)  # blank moves left to (2,1)
    assert puzzle.blank_position == (2, 1)

    puzzle.move(Puzzle.DOWN)  # blank moves up to (1,1)
    assert puzzle.blank_position == (1, 1)


def test_board_state_consistent_with_blank_position():
    """Board state matches blank_position."""
    puzzle = Puzzle(boardSize=3)
    puzzle.move(Puzzle.RIGHT)

    row, col = puzzle.blank_position
    assert puzzle.board[row][col] == 0
