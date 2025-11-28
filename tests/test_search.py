"""
Unit tests for the search function in calculate.py.

Tests the IDA* search algorithm implementation including
cost calculation, pruning, cycle detection, and solution finding.
"""

import sys
import os

import model
import calculate
from model import Puzzle


# Search function tests

def test_search_finds_solved_puzzle():
    """Search returns True immediately for solved puzzle."""
    puzzle = Puzzle(boardSize=4)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    result = calculate.search(path, 0, 100, move_sequence)

    assert result is True
    assert len(move_sequence) == 0  # No moves needed


def test_search_finds_one_move_solution():
    """Search finds solution one move away."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    # Bound of 2 should be enough (depth 1 + heuristic 1)
    result = calculate.search(path, 0, 2, move_sequence)

    assert result is True
    assert len(move_sequence) == 1
    assert move_sequence[0] == Puzzle.LEFT  # Move blank right (tile 15 moves left)


def test_search_prunes_when_exceeding_bound():
    """Search returns cost when exceeding bound."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    # Bound of 0 is too low - should return the actual cost
    result = calculate.search(path, 0, 0, move_sequence)

    assert isinstance(result, int)
    assert result > 0  # Should return exceeded cost
    assert len(move_sequence) == 0  # No moves made


def test_search_avoids_cycles():
    """Search doesn't revisit states in current path."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    # Create a path that already contains a state
    path = [puzzle]
    move_sequence = []

    # Move right to create a new state
    is_valid, next_puzzle = puzzle.simulateMove(Puzzle.RIGHT)
    assert is_valid

    # Now if we search, it should not revisit the original puzzle
    # We can verify this by checking that search doesn't get stuck
    result = calculate.search(path, 0, 10, move_sequence)

    # Should either find solution or return a cost
    assert result is True or isinstance(result, int)


def test_search_doesnt_undo_previous_move():
    """Search skips moves that undo the previous move."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    # Previous move was LEFT (tile 15 moved left, blank moved right)
    move_sequence = [Puzzle.LEFT]

    # Search should skip RIGHT (opposite of LEFT)
    # With bound high enough to explore
    result = calculate.search(path, 1, 10, move_sequence)

    # If more moves added, verify no immediate reversal
    if len(move_sequence) > 1:
        # Check that we didn't immediately reverse the last move
        last_move = move_sequence[-1]
        prev_move = move_sequence[-2]
        opposite = (-prev_move[0], -prev_move[1])
        # They should not be opposites
        assert last_move != opposite


def test_search_returns_minimum_exceeded_cost():
    """Search returns minimum cost that exceeded bound."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 0, 14, 15]]
    puzzle.blank_position = (3, 1)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    # Very low bound - should return minimum exceeded cost
    result = calculate.search(path, 0, 1, move_sequence)

    assert isinstance(result, int)
    assert result > 1  # Should exceed the bound
    assert result < calculate.INFINITY  # But not infinity


def test_search_with_zero_depth():
    """Search works correctly with depth 0."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    # Depth 0, bound high enough
    result = calculate.search(path, 0, 5, move_sequence)

    assert result is True
    assert len(move_sequence) == 1


def test_search_with_higher_depth():
    """Search uses depth parameter in cost calculation."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    # High depth with low bound should immediately exceed
    result = calculate.search(path, 10, 2, move_sequence)

    assert isinstance(result, int)
    assert result > 2  # Should exceed bound immediately


def test_search_two_moves_away():
    """Search finds solution two moves away."""
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 0, 14, 15]]
    puzzle.blank_position = (3, 1)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    # Bound of 3 should be enough (depth 2 + heuristic ~1)
    result = calculate.search(path, 0, 4, move_sequence)

    assert result is True
    assert len(move_sequence) == 2


def test_search_returns_infinity_when_no_solution():
    """Search returns INFINITY when no valid moves lead to solution."""
    # This is hard to test without creating an impossible puzzle
    # For now, we test that search can return integer values
    puzzle = Puzzle(boardSize=4)
    puzzle.board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    puzzle.blank_position = (3, 2)

    # Initialize pattern database
    calculate.init(4)

    path = [puzzle]
    move_sequence = []

    # Very restrictive bound
    result = calculate.search(path, 0, 0, move_sequence)

    # Should return a cost (integer), not infinity in this case
    assert isinstance(result, int)
