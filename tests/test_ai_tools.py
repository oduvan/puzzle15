"""
Unit tests for AI module functions.

Tests the heuristic calculation functions including Manhattan distance.
"""

import sys
import os
from unittest.mock import patch
import pytest

import model
import calculate
from model import Puzzle


# Fixtures

@pytest.fixture
def mock_no_manhattan():
    """
    Fixture that mocks calculate_manhattan_distance and ensures it's never called.

    This verifies that heuristic calculations use the pattern database
    instead of falling back to Manhattan distance.
    """
    with patch('calculate.calculate_manhattan_distance') as mock_manhattan:
        yield mock_manhattan
        # Verify it was never called after the test
        mock_manhattan.assert_not_called()


# Manhattan distance tests

def test_manhattan_distance_solved_puzzle():
    """Manhattan distance for solved puzzle is 0."""
    puzzle = Puzzle(boardSize=3)
    all_tiles = set(range(9))

    distance = calculate.calculate_manhattan_distance(puzzle, all_tiles)

    assert distance == 0


def test_manhattan_distance_one_tile_misplaced():
    """Manhattan distance for one tile one position away."""
    puzzle = Puzzle(boardSize=3)
    # Swap tiles 7 and 8: 7 should be at (2,0) but is at (2,1)
    puzzle.board = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
    all_tiles = set(range(9))

    distance = calculate.calculate_manhattan_distance(puzzle, all_tiles)

    # Tile 7: from (2,1) to (2,0) = 1 move
    # Tile 8: from (2,0) to (2,1) = 1 move
    # Total = 2
    assert distance == 2


def test_manhattan_distance_with_specific_group():
    """Manhattan distance for specific group of tiles only."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]

    # Only calculate for tile 7
    group = {7}
    distance = calculate.calculate_manhattan_distance(puzzle, group)

    # Tile 7: from (2,1) to (2,0) = 1 move
    assert distance == 1


def test_manhattan_distance_empty_group():
    """Manhattan distance for empty group is 0."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]

    group = set()
    distance = calculate.calculate_manhattan_distance(puzzle, group)

    assert distance == 0


def test_manhattan_distance_ignores_blank():
    """Manhattan distance ignores blank tile (0)."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    puzzle.blank_position = (1, 1)

    all_tiles = set(range(9))
    distance = calculate.calculate_manhattan_distance(puzzle, all_tiles)

    # Tile 5: from (1,2) to (1,1) = 1 move
    # Tile 6: from (2,0) to (1,2) = 1+2 = 3 moves
    # Tile 7: from (2,1) to (2,0) = 1 move
    # Tile 8: from (2,2) to (2,1) = 1 move
    # Total = 6 (blank is not counted)
    assert distance == 6


def test_manhattan_distance_4x4_solved():
    """Manhattan distance for solved 4x4 puzzle is 0."""
    puzzle = Puzzle(boardSize=4)
    all_tiles = set(range(16))

    distance = calculate.calculate_manhattan_distance(puzzle, all_tiles)

    assert distance == 0


def test_manhattan_distance_4x4_one_move():
    """Manhattan distance for 4x4 puzzle one move from solved."""
    puzzle = Puzzle(boardSize=4)
    # Move blank left once (15 moves right)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    all_tiles = set(range(16))
    distance = calculate.calculate_manhattan_distance(puzzle, all_tiles)

    # Tile 15: from (3,3) to (3,2) = 1 move
    assert distance == 1


def test_manhattan_distance_corner_to_corner():
    """Manhattan distance for tile moving from corner to opposite corner."""
    puzzle = Puzzle(boardSize=3)
    # Tile 1 at bottom-right, blank at top-left
    puzzle.board = [[0, 2, 3], [4, 5, 6], [7, 8, 1]]
    puzzle.blank_position = (0, 0)

    group = {1}
    distance = calculate.calculate_manhattan_distance(puzzle, group)

    # Tile 1: from (2,2) to (0,0) = 2+2 = 4 moves
    assert distance == 4


def test_manhattan_distance_multiple_tiles_in_group():
    """Manhattan distance for multiple specific tiles."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[3, 2, 1], [4, 5, 6], [7, 8, 0]]

    # Calculate for tiles 1, 2, 3
    group = {1, 2, 3}
    distance = calculate.calculate_manhattan_distance(puzzle, group)

    # Tile 1: from (0,2) to (0,0) = 2 moves
    # Tile 2: from (0,1) to (0,1) = 0 moves
    # Tile 3: from (0,0) to (0,2) = 2 moves
    # Total = 4
    assert distance == 4


def test_manhattan_distance_3x3_scrambled():
    """Manhattan distance for scrambled 3x3 puzzle."""
    puzzle = Puzzle(boardSize=3)
    puzzle.board = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
    puzzle.blank_position = (2, 2)

    all_tiles = set(range(9))
    distance = calculate.calculate_manhattan_distance(puzzle, all_tiles)

    # Tile 1: from (2,1) to (0,0) = 2+1 = 3
    # Tile 2: from (2,0) to (0,1) = 2+1 = 3
    # Tile 3: from (1,2) to (0,2) = 1+0 = 1
    # Tile 4: from (1,1) to (1,0) = 0+1 = 1
    # Tile 5: from (1,0) to (1,1) = 0+1 = 1
    # Tile 6: from (0,2) to (1,2) = 1+0 = 1
    # Tile 7: from (0,1) to (2,0) = 2+1 = 3
    # Tile 8: from (0,0) to (2,1) = 2+1 = 3
    # Total = 16
    assert distance == 16


def test_manhattan_distance_partial_group():
    """Manhattan distance for partial tile group matches expected value."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 14, 15, 12]]
    puzzle.blank_position = (2, 3)

    # Calculate for last row tiles only
    group = {12, 13, 14, 15}
    distance = calculate.calculate_manhattan_distance(puzzle, group)

    # Tile 12: from (3,3) to (2,3) = 1
    # Tile 13: from (3,0) to (3,0) = 0
    # Tile 14: from (3,1) to (3,1) = 0
    # Tile 15: from (3,2) to (3,2) = 0
    # Total = 1
    assert distance == 1


def test_manhattan_distance_tile_not_in_group_ignored():
    """Manhattan distance only counts tiles in specified group."""
    puzzle = Puzzle(boardSize=3)
    # All tiles wrong position
    puzzle.board = [[3, 2, 1], [6, 5, 4], [8, 7, 0]]

    # Only count tile 1
    group = {1}
    distance = calculate.calculate_manhattan_distance(puzzle, group)

    # Tile 1: from (0,2) to (0,0) = 2 moves
    # Other tiles ignored
    assert distance == 2


# Heuristic calculation tests (using pattern database)

def test_calculate_heuristic_solved_puzzle(mock_no_manhattan):
    """Heuristic for solved puzzle is 0."""
    puzzle = Puzzle(boardSize=4)

    # Initialize pattern database
    calculate.init(4)

    heuristic = calculate.calculate_heuristic(puzzle)

    assert heuristic == 0


def test_calculate_heuristic_one_move_away(mock_no_manhattan):
    """Heuristic for puzzle one move from solved."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    heuristic = calculate.calculate_heuristic(puzzle)

    # Should be at least 1 (one tile out of place)
    assert heuristic >= 1


def test_calculate_heuristic_uses_pattern_database(mock_no_manhattan):
    """Heuristic uses pattern database, not Manhattan distance."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 14, 15, 12]]
    puzzle.blank_position = (2, 3)

    # Initialize pattern database
    calculate.init(4)

    # Calculate heuristic (should use pattern DB, not print fallback message)
    heuristic = calculate.calculate_heuristic(puzzle)

    # Heuristic should be positive for unsolved puzzle
    assert heuristic > 0
    # Should be admissible (not overestimate)
    assert heuristic <= 10  # This puzzle is relatively close to solved


def test_calculate_heuristic_consistent(mock_no_manhattan):
    """Heuristic returns same value for same puzzle state."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 11], [13, 14, 15, 12]]
    puzzle.blank_position = (2, 2)

    # Initialize pattern database
    calculate.init(4)

    heuristic1 = calculate.calculate_heuristic(puzzle)
    heuristic2 = calculate.calculate_heuristic(puzzle)

    assert heuristic1 == heuristic2


def test_calculate_heuristic_admissible(mock_no_manhattan):
    """Heuristic is admissible (never overestimates)."""
    puzzle = Puzzle(boardSize=4)
    # Puzzle 2 moves from solved
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 0, 14, 15]]
    puzzle.blank_position = (3, 1)

    # Initialize pattern database
    calculate.init(4)

    heuristic = calculate.calculate_heuristic(puzzle)

    # Actual solution is 2 moves, heuristic should not exceed this
    assert heuristic <= 2


def test_calculate_heuristic_increases_with_distance(mock_no_manhattan):
    """Heuristic increases as puzzle gets further from solved state."""
    # Initialize pattern database once
    calculate.init(4)

    # Solved puzzle
    puzzle_solved = Puzzle(boardSize=4)
    h_solved = calculate.calculate_heuristic(puzzle_solved)

    # One move away
    puzzle_one = Puzzle(boardSize=4)
    puzzle_one.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle_one.blank_position = (3, 2)
    h_one = calculate.calculate_heuristic(puzzle_one)

    # Two moves away
    puzzle_two = Puzzle(boardSize=4)
    puzzle_two.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 0, 14, 15]]
    puzzle_two.blank_position = (3, 1)
    h_two = calculate.calculate_heuristic(puzzle_two)

    # Heuristic should increase with distance from goal
    assert h_solved == 0
    assert h_one > h_solved
    assert h_two >= h_one


def test_calculate_heuristic_nonnegative(mock_no_manhattan):
    """Heuristic is always non-negative."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[5, 1, 2, 4], [9, 6, 3, 8], [0, 10, 7, 11], [13, 14, 15, 12]]
    puzzle.blank_position = (2, 0)

    # Initialize pattern database
    calculate.init(4)

    heuristic = calculate.calculate_heuristic(puzzle)

    assert heuristic >= 0
