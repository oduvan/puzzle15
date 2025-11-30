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
    result, moved_tile = matrix.move(state, -1, 0)
    assert result == expected
    assert moved_tile == 3


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
    result, moved_tile = matrix.move(state, 1, 0)
    assert result == expected
    assert moved_tile == 7


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
    result, moved_tile = matrix.move(state, 0, -1)
    assert result == expected
    assert moved_tile == 6


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
    result, moved_tile = matrix.move(state, 0, 1)
    assert result == expected
    assert moved_tile == 8


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
    result, moved_tile = matrix.move(state, -1, -1)
    assert result == expected
    assert moved_tile == 2


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
    result, moved_tile = matrix.move(state, 1, -2)
    assert result == expected
    assert moved_tile == 13


# Invalid move tests

def test_move_up_from_top_edge():
    """Moving up from top row returns (None, None)."""
    state = matrix.square_to_flat((
        (1, 2, 0, 4),
        (5, 6, 3, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result = matrix.move(state, -1, 0)
    assert result == (None, None)


def test_move_down_from_bottom_edge():
    """Moving down from bottom row returns (None, None)."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))
    result = matrix.move(state, 1, 0)
    assert result == (None, None)


def test_move_left_from_left_edge():
    """Moving left from left column returns (None, None)."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (0, 6, 7, 8),
        (5, 10, 11, 12),
        (13, 14, 15, 9)
    ))
    result = matrix.move(state, 0, -1)
    assert result == (None, None)


def test_move_right_from_right_edge():
    """Moving right from right column returns (None, None)."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 0),
        (9, 10, 11, 8),
        (13, 14, 15, 12)
    ))
    result = matrix.move(state, 0, 1)
    assert result == (None, None)


def test_move_out_of_bounds_diagonal():
    """Moving diagonally out of bounds returns (None, None)."""
    state = matrix.square_to_flat((
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11),
        (12, 13, 14, 15)
    ))
    result = matrix.move(state, -1, -1)
    assert result == (None, None)


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
    result, moved_tile = matrix.move(state, -1, 0)
    assert result == expected
    assert moved_tile == 2


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
    result, moved_tile = matrix.move(state, 0, 1)
    assert result == expected
    assert moved_tile == 6


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
    result, moved_tile = matrix.move(state, -1, 0)

    assert state == original_state
    assert result != state
    assert isinstance(result, tuple)
    assert isinstance(moved_tile, int)
    assert moved_tile == 3


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


# Replace with zeros tests

def test_replace_with_zeros_empty_set():
    """Keeping empty set zeros everything."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    result = matrix.replace_with_zeros(state, set())
    expected = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert result == expected


def test_replace_with_zeros_single_tile():
    """Keep only a single tile."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    result = matrix.replace_with_zeros(state, {5})
    expected = (0, 0, 0, 0, 5, 0, 0, 0, 0)
    assert result == expected


def test_replace_with_zeros_multiple_tiles():
    """Keep only multiple specified tiles."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    result = matrix.replace_with_zeros(state, {1, 2})
    expected = (1, 2, 0, 0, 0, 0, 0, 0, 0)
    assert result == expected


def test_replace_with_zeros_half_tiles_3x3():
    """Keep half the tiles in 3x3 puzzle."""
    state = matrix.square_to_flat((
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    ))
    result = matrix.replace_with_zeros(state, {1, 2, 5, 8})
    expected = matrix.square_to_flat((
        (1, 2, 0),
        (0, 5, 0),
        (0, 8, 0)
    ))
    assert result == expected


def test_replace_with_zeros_half_tiles_4x4():
    """Keep half the tiles in 4x4 puzzle."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    result = matrix.replace_with_zeros(state, {1, 2, 3, 4, 9, 10, 11, 12})
    expected = matrix.square_to_flat((
        (1, 2, 3, 4),
        (0, 0, 0, 0),
        (9, 10, 11, 12),
        (0, 0, 0, 0)
    ))
    assert result == expected


def test_replace_with_zeros_nonexistent_tiles():
    """Keeping nonexistent tiles zeros everything."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    result = matrix.replace_with_zeros(state, {10, 11, 12})
    expected = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert result == expected


def test_replace_with_zeros_returns_tuple():
    """replace_with_zeros returns a tuple."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    result = matrix.replace_with_zeros(state, {5})
    assert isinstance(result, tuple)


def test_replace_with_zeros_immutable():
    """replace_with_zeros doesn't modify original state."""
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    original = state
    result = matrix.replace_with_zeros(state, {1, 2, 6, 7, 8})
    assert state == original
    assert result != state


# Edge case tests

def test_move_zero_steps():
    """Moving zero steps returns same position."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 0, 8),
        (9, 10, 7, 12),
        (13, 14, 11, 15)
    ))
    result, moved_tile = matrix.move(state, 0, 0)
    assert result == state
    assert moved_tile == 0  # Blank swaps with itself


def test_move_from_corner_top_left():
    """Test moves from top-left corner."""
    state = matrix.square_to_flat((
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11),
        (12, 13, 14, 15)
    ))
    assert matrix.move(state, -1, 0) == (None, None)  # Can't move up
    assert matrix.move(state, 0, -1) == (None, None)  # Can't move left
    assert matrix.move(state, 1, 0) != (None, None)  # Can move down
    assert matrix.move(state, 0, 1) != (None, None)  # Can move right


def test_move_from_corner_bottom_right():
    """Test moves from bottom-right corner."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    ))
    assert matrix.move(state, 1, 0) == (None, None)  # Can't move down
    assert matrix.move(state, 0, 1) == (None, None)  # Can't move right
    assert matrix.move(state, -1, 0) != (None, None)  # Can move up
    assert matrix.move(state, 0, -1) != (None, None)  # Can move left


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
    result, moved_tile = matrix.move(solved, 0, -1)
    assert result == expected
    assert moved_tile == 15


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
    result, moved_tile = matrix.move(solved, -1, 0)
    assert result == expected
    assert moved_tile == 6


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


def test_manhattan_distance_half_zeros_3x3():
    """Manhattan distance with half elements being zero (3x3)."""
    current = matrix.square_to_flat((
        (1, 2, 0),
        (0, 5, 0),
        (0, 8, 0)
    ))
    goal = matrix.square_to_flat((
        (1, 0, 0),
        (0, 0, 2),
        (5, 8, 0)
    ))
    distance = matrix.manhattan_distance(current, goal)
    assert distance == 4


def test_manhattan_distance_half_zeros_4x4():
    """Manhattan distance with half elements being zero (4x4)."""
    current = matrix.square_to_flat((
        (1, 2, 3, 4),
        (0, 0, 0, 0),
        (9, 10, 11, 12),
        (0, 0, 0, 0)
    ))
    goal = matrix.square_to_flat((
        (0, 0, 0, 0),
        (1, 2, 3, 4),
        (0, 0, 0, 0),
        (9, 10, 11, 12)
    ))
    distance = matrix.manhattan_distance(current, goal)
    assert distance == 8


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


def test_manhattan_distance_to_win_half_zeros_3x3():
    """Manhattan distance to win with half elements being zero (3x3)."""
    current = matrix.square_to_flat((
        (2, 1, 0),
        (0, 8, 0),
        (0, 5, 0)
    ))
    distance = matrix.manhattan_distance_to_win(current)
    assert distance == 4


def test_manhattan_distance_to_win_half_zeros_4x4():
    """Manhattan distance to win with half elements being zero (4x4)."""
    current = matrix.square_to_flat((
        (2, 1, 4, 3),
        (0, 0, 0, 0),
        (12, 11, 10, 9),
        (0, 0, 0, 0)
    ))
    distance = matrix.manhattan_distance_to_win(current)
    assert distance == 12


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


# Move compression tests

def test_compress_moves_empty_sequence():
    """Compress empty move sequence."""
    moves = []
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == []
    assert (packed & 0xFF) == 0  # Length should be 0


def test_compress_moves_single_up():
    """Compress single upward move."""
    moves = [(-1, 0)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves
    assert (packed & 0xFF) == 1  # Length should be 1


def test_compress_moves_single_down():
    """Compress single downward move."""
    moves = [(1, 0)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves


def test_compress_moves_single_left():
    """Compress single left move."""
    moves = [(0, -1)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves


def test_compress_moves_single_right():
    """Compress single right move."""
    moves = [(0, 1)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves


def test_compress_moves_all_directions():
    """Compress sequence with all four directions."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves
    assert (packed & 0xFF) == 4  # Length should be 4


def test_compress_moves_long_sequence():
    """Compress longer move sequence."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 0), (0, 1), (1, 0)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves
    assert (packed & 0xFF) == 7  # Length should be 7


def test_compress_moves_very_long_sequence():
    """Compress very long move sequence (50 moves)."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] * 12 + [(1, 0), (0, -1)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves
    assert len(unpacked) == 50


def test_compress_moves_repeated_moves():
    """Compress sequence with repeated same moves."""
    moves = [(-1, 0)] * 10
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves
    assert all(m == (-1, 0) for m in unpacked)


def test_compress_moves_returns_integer():
    """Compress moves returns an integer."""
    moves = [(-1, 0), (0, 1), (1, 0)]
    packed = matrix.compress_moves(moves)
    assert isinstance(packed, int)
    assert packed >= 0


def test_compress_moves_different_sequences_different_values():
    """Different move sequences compress to different integers."""
    moves1 = [(-1, 0), (1, 0), (0, -1)]
    moves2 = [(-1, 0), (1, 0), (0, 1)]
    packed1 = matrix.compress_moves(moves1)
    packed2 = matrix.compress_moves(moves2)
    assert packed1 != packed2


def test_compress_moves_order_matters():
    """Move order affects compressed value."""
    moves1 = [(-1, 0), (1, 0)]
    moves2 = [(1, 0), (-1, 0)]
    packed1 = matrix.compress_moves(moves1)
    packed2 = matrix.compress_moves(moves2)
    assert packed1 != packed2


def test_compress_moves_length_embedded():
    """Length is properly embedded in lower 8 bits."""
    for length in [1, 5, 10, 20, 50, 100]:
        moves = [(-1, 0)] * length
        packed = matrix.compress_moves(moves)
        extracted_length = packed & 0xFF
        assert extracted_length == length


def test_compress_moves_roundtrip_typical_solution():
    """Roundtrip for typical puzzle solution sequence."""
    moves = [
        (1, 0), (0, 1), (-1, 0), (-1, 0),
        (0, -1), (1, 0), (1, 0), (0, 1)
    ]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves


def test_compress_moves_memory_efficiency():
    """Verify compression is memory efficient."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] * 10  # 40 moves
    packed = matrix.compress_moves(moves)

    # Packed should be much smaller than storing 40 tuples
    # 40 moves * 2 bits = 80 bits + 8 bits length = 88 bits = 11 bytes
    # vs 40 tuples * ~16 bytes each = ~640 bytes
    assert packed.bit_length() <= 88


def test_compress_moves_max_length():
    """Test with maximum reasonable length (255 moves)."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] * 63 + [(1, 0), (0, -1), (-1, 0)]
    assert len(moves) == 255
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert unpacked == moves
    assert len(unpacked) == 255


def test_decompress_moves_returns_list():
    """Decompress moves returns a list."""
    moves = [(-1, 0), (0, 1), (1, 0)]
    packed = matrix.compress_moves(moves)
    unpacked = matrix.decompress_moves(packed)
    assert isinstance(unpacked, list)


def test_compress_moves_encoding_values():
    """Verify specific encoding values for moves."""
    # Up should be 00, Down 01, Left 10, Right 11
    up = matrix.compress_moves([(-1, 0)])
    down = matrix.compress_moves([(1, 0)])
    left = matrix.compress_moves([(0, -1)])
    right = matrix.compress_moves([(0, 1)])

    # Extract just the move bits (skip length byte)
    assert (up >> 8) == 0b00
    assert (down >> 8) == 0b01
    assert (left >> 8) == 0b10
    assert (right >> 8) == 0b11


def test_get_moves_length_empty():
    """Get length of empty move sequence."""
    packed = matrix.compress_moves([])
    length = matrix.get_moves_length(packed)
    assert length == 0


def test_get_moves_length_single():
    """Get length of single move."""
    packed = matrix.compress_moves([(-1, 0)])
    length = matrix.get_moves_length(packed)
    assert length == 1


def test_get_moves_length_multiple():
    """Get length of multiple moves."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    packed = matrix.compress_moves(moves)
    length = matrix.get_moves_length(packed)
    assert length == 4


def test_get_moves_length_matches_decompress():
    """get_moves_length should match len(decompress_moves())."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 0), (0, 1)]
    packed = matrix.compress_moves(moves)

    length_fast = matrix.get_moves_length(packed)
    length_slow = len(matrix.decompress_moves(packed))

    assert length_fast == length_slow == len(moves)


def test_get_moves_length_long_sequence():
    """Get length of long move sequence."""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] * 25  # 100 moves
    packed = matrix.compress_moves(moves)
    length = matrix.get_moves_length(packed)
    assert length == 100
