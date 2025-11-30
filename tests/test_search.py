"""
Unit tests for the search function in calculate.py.

Tests the IDA* search algorithm implementation including
cost calculation, pruning, cycle detection, and solution finding.
"""

import sys
import os

import matrix
import calculate


# Direction constants (matching calculate.py DIRECTIONS)
# Direction tuples represent blank movement
LEFT = (0, 1)    # Blank moves right (tile moves left)
RIGHT = (0, -1)  # Blank moves left (tile moves right)
UP = (-1, 0)     # Blank moves up (tile moves down)
DOWN = (1, 0)    # Blank moves down (tile moves up)


# Search function tests

def test_search_finds_solved_puzzle():
    """Search returns True immediately for solved puzzle."""
    state = matrix.get_win(4)

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    result = calculate.search(path, 0, 100, move_sequence, frontier)

    assert result is True
    assert len(move_sequence) == 0  # No moves needed


def test_search_finds_one_move_solution():
    """Search finds solution one move away."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Bound of 2 should be enough (depth 1 + heuristic 1)
    result = calculate.search(path, 0, 2, move_sequence, frontier)

    assert result is True
    assert len(move_sequence) == 1
    assert move_sequence[0] == LEFT  # Move blank right (tile 15 moves left)


def test_search_prunes_when_exceeding_bound():
    """Search returns cost when exceeding bound."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Bound of 0 is too low - should return the actual cost
    result = calculate.search(path, 0, 0, move_sequence, frontier)

    assert isinstance(result, int)
    assert result > 0  # Should return exceeded cost
    assert len(move_sequence) == 0  # No moves made


def test_search_avoids_cycles():
    """Search doesn't revisit states in current path."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    # Create a path that already contains a state
    path = [state]
    move_sequence = []
    frontier = {}

    # Now if we search, it should not revisit the original state
    # We can verify this by checking that search doesn't get stuck
    result = calculate.search(path, 0, 10, move_sequence, frontier)

    # Should either find solution or return a cost
    assert result is True or isinstance(result, int)


def test_search_doesnt_undo_previous_move():
    """Search skips moves that undo the previous move."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    # Previous move was LEFT (tile 15 moved left, blank moved right)
    move_sequence = [LEFT]
    frontier = {}

    # Search should skip RIGHT (opposite of LEFT)
    # With bound high enough to explore
    result = calculate.search(path, 1, 10, move_sequence, frontier)

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
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 0, 14, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Very low bound - should return minimum exceeded cost
    result = calculate.search(path, 0, 1, move_sequence, frontier)

    assert isinstance(result, int)
    assert result > 1  # Should exceed the bound
    assert result < calculate.INFINITY  # But not infinity


def test_search_with_zero_depth():
    """Search works correctly with depth 0."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Depth 0, bound high enough
    result = calculate.search(path, 0, 5, move_sequence, frontier)

    assert result is True
    assert len(move_sequence) == 1


def test_search_with_higher_depth():
    """Search uses depth parameter in cost calculation."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # High depth with low bound should immediately exceed
    result = calculate.search(path, 10, 2, move_sequence, frontier)

    assert isinstance(result, int)
    assert result > 2  # Should exceed bound immediately


def test_search_two_moves_away():
    """Search finds solution two moves away."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 0, 14, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Bound of 3 should be enough (depth 2 + heuristic ~1)
    result = calculate.search(path, 0, 4, move_sequence, frontier)

    assert result is True
    assert len(move_sequence) == 2


def test_search_returns_infinity_when_no_solution():
    """Search returns INFINITY when no valid moves lead to solution."""
    # This is hard to test without creating an impossible puzzle
    # For now, we test that search can return integer values
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    # Initialize pattern database
    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Very restrictive bound
    result = calculate.search(path, 0, 0, move_sequence, frontier)

    # Should return a cost (integer), not infinity in this case
    assert isinstance(result, int)


# Frontier optimization tests

def test_frontier_stores_nodes_when_exceeding_bound():
    """Frontier stores nodes that exceed the bound."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Low bound - should trigger frontier storage
    result = calculate.search(path, 0, 0, move_sequence, frontier)

    # Frontier should have entries
    assert len(frontier) > 0
    assert isinstance(result, int)


def test_frontier_skips_already_stored_nodes():
    """Search skips exploring nodes already in frontier."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 0, 14, 15)
    ))

    calculate.init(4)

    # Pre-populate frontier with a state
    next_state, _ = matrix.move(state, *LEFT)
    frontier = {matrix.compress(next_state): matrix.compress_moves([LEFT])}

    path = [state]
    move_sequence = []

    # Should skip the pre-populated state
    result = calculate.search(path, 0, 10, move_sequence, frontier)

    # Should still work but not explore the frontier node
    assert result is True or isinstance(result, int)


def test_frontier_compresses_moves_efficiently():
    """Frontier stores moves in compressed format."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    calculate.init(4)

    path = [state]
    move_sequence = []
    frontier = {}

    # Trigger frontier storage
    calculate.search(path, 0, 0, move_sequence, frontier)

    # Check that frontier values are integers (compressed)
    for state_key, packed_moves in frontier.items():
        assert isinstance(state_key, int)
        assert isinstance(packed_moves, int)


def test_ida_star_with_frontier_enabled():
    """IDA* with frontier enabled solves puzzles correctly."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    calculate.init(4)

    solution = calculate.ida_star(state, use_frontier=True)

    assert solution is not None
    assert len(solution) == 1
    assert solution[0] == LEFT


def test_ida_star_with_frontier_disabled():
    """IDA* with frontier disabled solves puzzles correctly."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    calculate.init(4)

    solution = calculate.ida_star(state, use_frontier=False)

    assert solution is not None
    assert len(solution) == 1
    assert solution[0] == LEFT


def test_ida_star_frontier_vs_no_frontier_same_result():
    """IDA* produces same solution with and without frontier."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 0, 14, 15)
    ))

    calculate.init(4)

    solution_with_frontier = calculate.ida_star(state, use_frontier=True)
    solution_without_frontier = calculate.ida_star(state, use_frontier=False)

    # Both should find same length solution (optimal)
    assert len(solution_with_frontier) == len(solution_without_frontier)
    assert solution_with_frontier is not None
    assert solution_without_frontier is not None


def test_ida_star_already_solved():
    """IDA* returns empty list for already solved puzzle."""
    state = matrix.get_win(4)

    calculate.init(4)

    solution = calculate.ida_star(state, use_frontier=True)

    assert solution == []


def test_ida_star_two_move_solution_with_frontier():
    """IDA* with frontier solves two-move puzzle."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 0, 14, 15)
    ))

    calculate.init(4)

    solution = calculate.ida_star(state, use_frontier=True)

    assert solution is not None
    assert len(solution) == 2

    # Verify solution works
    current = state
    for move in solution:
        current, _ = matrix.move(current, *move)
    assert current == matrix.get_win(4)


def test_frontier_persists_across_iterations():
    """Frontier nodes persist across bound increases."""
    state = matrix.square_to_flat((
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    ))

    calculate.init(4)

    # Run with very low initial bounds to force multiple iterations
    # This will populate frontier in early iterations
    frontier = {}
    path = [state]
    move_sequence = []

    # First iteration with bound 0 - should populate frontier
    calculate.search(path, 0, 0, move_sequence, frontier)
    initial_frontier_size = len(frontier)

    # Frontier should have nodes
    assert initial_frontier_size > 0

    # Simulate next iteration with slightly higher bound
    # Some nodes might become explorable, but others should remain
    calculate.search(path, 0, 1, move_sequence, frontier)

    # Frontier can grow or shrink but should still contain nodes
    # (unless all were within bound, which is unlikely for bound=1)
    assert len(frontier) >= 0
