"""
Unit tests for matrix module.

Tests the flat array (tuple) representation of N-puzzle and operations
including move, conversions, and size calculations.
"""

import pytest
import matrix
from matrix import TFlat, TSquare


# Size calculation tests

def test_get_size_by_length_3x3():
    """Size calculation works for 3x3 puzzle (9 elements)."""
    assert matrix._get_size_by_length(9) == 3


def test_get_size_by_length_4x4():
    """Size calculation works for 4x4 puzzle (16 elements)."""
    assert matrix._get_size_by_length(16) == 4


def test_get_size_by_length_5x5():
    """Size calculation works for 5x5 puzzle (25 elements)."""
    assert matrix._get_size_by_length(25) == 5


def test_get_size_by_length_caching():
    """Verify caching works by calling twice with same value."""
    # Clear cache first
    matrix._get_size_by_length.cache_clear()

    # First call
    result1 = matrix._get_size_by_length(16)
    cache_info1 = matrix._get_size_by_length.cache_info()

    # Second call - should hit cache
    result2 = matrix._get_size_by_length(16)
    cache_info2 = matrix._get_size_by_length.cache_info()

    assert result1 == result2 == 4
    assert cache_info1.hits == 0
    assert cache_info2.hits == 1


def test_get_size_3x3():
    """get_size works for 3x3 tuple."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    assert matrix.get_size(state) == 3


def test_get_size_4x4():
    """get_size works for 4x4 tuple."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    assert matrix.get_size(state) == 4


def test_get_size_5x5():
    """get_size works for 5x5 tuple."""
    state = tuple(range(0, 25))
    assert matrix.get_size(state) == 5


# Move function tests - 4x4 puzzle

def test_move_up_valid():
    """Move blank space up from middle position."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 0, 4),
        (5, 6, 3, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, -1, 0)
    assert result == expected


def test_move_down_valid():
    """Move blank space down from middle position."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 0, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, 1, 0)
    assert result == expected


def test_move_left_valid():
    """Move blank space left from middle position."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 0, 6, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, 0, -1)
    assert result == expected


def test_move_right_valid():
    """Move blank space right from middle position."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 8, 0),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, 0, 1)
    assert result == expected


def test_move_diagonal_valid():
    """Move blank space diagonally (up and left)."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    expected = matrix.square_to_flat((
        (1, 0, 3, 4),
        (5, 6, 2, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, -1, -1)
    assert result == expected


def test_move_multiple_steps():
    """Move blank space by multiple steps."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 0, 12),
        (13, 14, 11, 15)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 13, 12),
        (0, 14, 11, 15)
    ))
    result = matrix.move(state, 1, -2)
    assert result == expected


# Invalid move tests

def test_move_up_from_top_edge():
    """Moving up from top row returns None."""
    state = matrix.square_to_flat((
        (1, 2, 0, 4),
        (5, 6, 3, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, -1, 0)
    assert result is None


def test_move_down_from_bottom_edge():
    """Moving down from bottom row returns None."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))
    result = matrix.move(state, 1, 0)
    assert result is None


def test_move_left_from_left_edge():
    """Moving left from left column returns None."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (0, 6, 7, 8),
        (5, 10, 11, 12),
        (13, 14, 15, 9)
    ))
    result = matrix.move(state, 0, -1)
    assert result is None


def test_move_right_from_right_edge():
    """Moving right from right column returns None."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 0),
        (9, 10, 11, 8),
        (13, 14, 15, 12)
    ))
    result = matrix.move(state, 0, 1)
    assert result is None


def test_move_out_of_bounds_diagonal():
    """Moving diagonally out of bounds returns None."""
    state = matrix.square_to_flat((
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11),
        (12, 13, 14, 15)
    ))
    result = matrix.move(state, -1, -1)
    assert result is None


# Move tests - 3x3 puzzle

def test_move_3x3_up():
    """Move works on 3x3 puzzle - up."""
    state = matrix.square_to_flat((
        (1, 2, 3),
        (4, 0, 6),
        (7, 8, 5)
    ))
    expected = matrix.square_to_flat((
        (1, 0, 3),
        (4, 2, 6),
        (7, 8, 5)
    ))
    result = matrix.move(state, -1, 0)
    assert result == expected


def test_move_3x3_right():
    """Move works on 3x3 puzzle - right."""
    state = matrix.square_to_flat((
        (1, 2, 3),
        (4, 0, 6),
        (7, 8, 5)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 3),
        (4, 6, 0),
        (7, 8, 5)
    ))
    result = matrix.move(state, 0, 1)
    assert result == expected


# Immutability tests

def test_move_returns_new_tuple():
    """Move returns a new tuple, not modifying the original."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    original_state = state
    result = matrix.move(state, -1, 0)

    assert state == original_state
    assert result != state
    assert isinstance(result, tuple)


def test_state_is_hashable():
    """Tuple states can be used as dictionary keys."""
    state1 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    state2 = (1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 7, 12, 13, 14, 11, 15)

    # Should be able to use states as dict keys
    state_dict = {state1: "solved", state2: "scrambled"}

    assert state_dict[state1] == "solved"
    assert state_dict[state2] == "scrambled"


def test_state_can_be_in_set():
    """Tuple states can be added to sets."""
    state1 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    state2 = (1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 7, 12, 13, 14, 11, 15)

    state_set = {state1, state2}

    assert len(state_set) == 2
    assert state1 in state_set
    assert state2 in state_set


# Conversion tests

def test_flat_to_square_4x4():
    """flat_to_square converts 4x4 flat array to matrix."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    result = matrix.flat_to_square(state)

    expected = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    )
    assert result == expected
    assert isinstance(result, tuple)
    assert all(isinstance(row, tuple) for row in result)


def test_flat_to_square_3x3():
    """flat_to_square converts 3x3 flat array to matrix."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    result = matrix.flat_to_square(state)

    expected = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    )
    assert result == expected


def test_square_to_flat_4x4():
    """square_to_flat converts 4x4 matrix to flat array."""
    square = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    )
    result = matrix.square_to_flat(square)

    expected = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    assert result == expected
    assert isinstance(result, tuple)


def test_square_to_flat_3x3():
    """square_to_flat converts 3x3 matrix to flat array."""
    square = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    )
    result = matrix.square_to_flat(square)

    expected = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    assert result == expected


def test_flat_to_square_to_flat_roundtrip():
    """Converting flat->square->flat returns original."""
    original = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)

    square = matrix.flat_to_square(original)
    result = matrix.square_to_flat(square)

    assert result == original


def test_square_to_flat_to_square_roundtrip():
    """Converting square->flat->square returns original."""
    original = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    )

    flat = matrix.square_to_flat(original)
    result = matrix.flat_to_square(flat)

    assert result == original


# Edge case tests

def test_move_zero_steps():
    """Moving zero steps returns same position."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, 0, 0)
    assert result == state


def test_move_from_corner_top_left():
    """Test moves from top-left corner."""
    state = matrix.square_to_flat((
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11),
        (12, 13, 14, 15)
    ))
    assert matrix.move(state, -1, 0) is None  # Can't move up
    assert matrix.move(state, 0, -1) is None  # Can't move left
    assert matrix.move(state, 1, 0) is not None  # Can move down
    assert matrix.move(state, 0, 1) is not None  # Can move right


def test_move_from_corner_bottom_right():
    """Test moves from bottom-right corner."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    assert matrix.move(state, 1, 0) is None  # Can't move down
    assert matrix.move(state, 0, 1) is None  # Can't move right
    assert matrix.move(state, -1, 0) is not None  # Can move up
    assert matrix.move(state, 0, -1) is not None  # Can move left


def test_solved_state_4x4():
    """Test with solved 4x4 puzzle."""
    solved = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))
    result = matrix.move(solved, 0, -1)
    assert result == expected


def test_solved_state_3x3():
    """Test with solved 3x3 puzzle."""
    solved = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    expected = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 0),
        (7, 8, 6)
    ))
    result = matrix.move(solved, -1, 0)
    assert result == expected


# Manhattan distance tests

def test_manhattan_distance_solved_state():
    """Manhattan distance for solved state is 0."""
    solved = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    distance = matrix.manhattan_distance(solved, solved)
    assert distance == 0


def test_manhattan_distance_one_move():
    """Manhattan distance for state one move from goal."""
    current = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))
    goal = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    distance = matrix.manhattan_distance(current, goal)
    assert distance == 1


def test_manhattan_distance_multiple_tiles():
    """Manhattan distance with multiple tiles out of place."""
    current = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    goal = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    distance = matrix.manhattan_distance(current, goal)
    assert distance == 3


def test_manhattan_distance_3x3():
    """Manhattan distance works for 3x3 puzzle."""
    current = matrix.square_to_flat((
        (1, 2, 3),
        (4, 0, 6),
        (7, 5, 8)
    ))
    goal = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    distance = matrix.manhattan_distance(current, goal)
    assert distance == 2


def test_manhattan_distance_worst_case_3x3():
    """Manhattan distance for worst case 3x3."""
    current = matrix.square_to_flat((
        (8, 7, 6),
        (5, 4, 3),
        (2, 1, 0)
    ))
    goal = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    distance = matrix.manhattan_distance(current, goal)
    assert distance == 16


def test_manhattan_distance_different_goals():
    """Manhattan distance works with different goal states."""
    current = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    goal = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 0),
        (13, 14, 15, 12)
    ))
    distance = matrix.manhattan_distance(current, goal)
    assert distance == 1


# Manhattan distance to win tests

def test_manhattan_distance_to_win_solved_3x3():
    """Manhattan distance to win for solved 3x3 is 0."""
    solved = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    distance = matrix.manhattan_distance_to_win(solved)
    assert distance == 0


def test_manhattan_distance_to_win_solved_4x4():
    """Manhattan distance to win for solved 4x4 is 0."""
    solved = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    distance = matrix.manhattan_distance_to_win(solved)
    assert distance == 0


def test_manhattan_distance_to_win_one_move_4x4():
    """Manhattan distance to win one move away."""
    current = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))
    distance = matrix.manhattan_distance_to_win(current)
    assert distance == 1


def test_manhattan_distance_to_win_multiple_tiles_4x4():
    """Manhattan distance to win with multiple tiles out of place."""
    current = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    distance = matrix.manhattan_distance_to_win(current)
    assert distance == 3


def test_manhattan_distance_to_win_3x3():
    """Manhattan distance to win works for 3x3."""
    current = matrix.square_to_flat((
        (1, 2, 3),
        (4, 0, 6),
        (7, 5, 8)
    ))
    distance = matrix.manhattan_distance_to_win(current)
    assert distance == 2


def test_manhattan_distance_to_win_worst_case_3x3():
    """Manhattan distance to win for worst case 3x3."""
    current = matrix.square_to_flat((
        (8, 7, 6),
        (5, 4, 3),
        (2, 1, 0)
    ))
    distance = matrix.manhattan_distance_to_win(current)
    assert distance == 16


def test_manhattan_distance_to_win_matches_general():
    """manhattan_distance_to_win matches manhattan_distance for winning goal."""
    current = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    goal = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))

    distance_general = matrix.manhattan_distance(current, goal)
    distance_to_win = matrix.manhattan_distance_to_win(current)

    assert distance_general == distance_to_win


# Compress/Decompress tests

def test_compress_decompress_3x3_solved():
    """Compress and decompress roundtrip for solved 3x3."""
    original = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    compressed = matrix.compress(original)
    decompressed = matrix.decompress(compressed, 3)
    assert decompressed == original


def test_compress_decompress_4x4_solved():
    """Compress and decompress roundtrip for solved 4x4."""
    original = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    compressed = matrix.compress(original)
    decompressed = matrix.decompress(compressed, 4)
    assert decompressed == original


def test_compress_decompress_5x5_solved():
    """Compress and decompress roundtrip for solved 5x5."""
    original = tuple(range(1, 25)) + (0,)
    compressed = matrix.compress(original)
    decompressed = matrix.decompress(compressed, 5)
    assert decompressed == original


def test_compress_decompress_3x3_scrambled():
    """Compress and decompress roundtrip for scrambled 3x3."""
    original = matrix.square_to_flat((
        (8, 7, 6),
        (5, 4, 3),
        (2, 1, 0)
    ))
    compressed = matrix.compress(original)
    decompressed = matrix.decompress(compressed, 3)
    assert decompressed == original


def test_compress_decompress_4x4_scrambled():
    """Compress and decompress roundtrip for scrambled 4x4."""
    original = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    compressed = matrix.compress(original)
    decompressed = matrix.decompress(compressed, 4)
    assert decompressed == original


def test_compress_returns_integer():
    """Compress returns an integer."""
    state = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    compressed = matrix.compress(state)
    assert isinstance(compressed, int)
    assert compressed >= 0


def test_compress_different_states_different_values():
    """Different states compress to different integers."""
    state1 = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    state2 = matrix.square_to_flat((
        (1, 2, 3),
        (4, 0, 6),
        (7, 5, 8)
    ))
    compressed1 = matrix.compress(state1)
    compressed2 = matrix.compress(state2)
    assert compressed1 != compressed2


def test_decompress_returns_tuple():
    """Decompress returns a tuple."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    compressed = matrix.compress(state)
    decompressed = matrix.decompress(compressed, 4)
    assert isinstance(decompressed, tuple)
    assert len(decompressed) == 16


def test_compress_all_zeros():
    """Compress handles all zeros correctly."""
    original = tuple([0] * 9)
    compressed = matrix.compress(original)
    decompressed = matrix.decompress(compressed, 3)
    assert decompressed == original
    assert compressed == 0


def test_compress_max_values_3x3():
    """Compress handles maximum values for 3x3."""
    original = (8, 7, 6, 5, 4, 3, 2, 1, 0)
    compressed = matrix.compress(original)
    decompressed = matrix.decompress(compressed, 3)
    assert decompressed == original
