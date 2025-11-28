"""
End-to-end tests for play_console.py.

Tests the console solver with simple 4x4 puzzles to verify correct move sequences.
"""

import subprocess
import sys
import os

def run_console_solver(puzzle_input):
    """Run play_console.py with given input and return output."""
    result = subprocess.run(
        ['python3', 'play_console.py'],
        input=puzzle_input,
        capture_output=True,
        text=True,
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    return result.stdout, result.returncode


def test_solved_puzzle():
    """Console solver should recognize an already solved puzzle."""
    puzzle_input = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0"

    output, returncode = run_console_solver(puzzle_input)

    assert returncode == 0, "Should exit successfully"
    assert "already solved" in output.lower(), "Should indicate puzzle is already solved"


def test_one_move_puzzle():
    """Console solver should solve a 1-move puzzle with correct move."""
    # Puzzle that's one move away from solved
    # Solution: LEFT (tile 15 moves left into blank space)
    puzzle_input = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15"

    output, returncode = run_console_solver(puzzle_input)

    assert returncode == 0, "Should exit successfully"
    assert "Total moves: 1" in output, "Should report 1 move"
    assert "Move sequence: LEFT" in output, "Move sequence should be: LEFT"
    assert "Step 1: Move LEFT" in output, "Should show Step 1: Move LEFT"


def test_two_move_puzzle():
    """Console solver should solve a 2-move puzzle with correct sequence."""
    # Puzzle that's two moves away from solved
    # Solution: LEFT -> LEFT
    puzzle_input = "1 2 3 4 5 6 7 8 9 10 11 12 13 0 14 15"

    output, returncode = run_console_solver(puzzle_input)

    assert returncode == 0, "Should exit successfully"
    assert "Total moves: 2" in output, "Should report 2 moves"
    assert "Move sequence: LEFT -> LEFT" in output, "Move sequence should be: LEFT -> LEFT"
    assert "Step 1: Move LEFT" in output, "Should show Step 1: Move LEFT"
    assert "Step 2: Move LEFT" in output, "Should show Step 2: Move LEFT"


def test_three_move_puzzle():
    """Console solver should solve a 3-move puzzle with correct sequence."""
    # Puzzle that's three moves away from solved
    # Solution: UP -> LEFT -> UP
    puzzle_input = "1 2 3 4 5 6 0 8 9 10 7 11 13 14 15 12"

    output, returncode = run_console_solver(puzzle_input)

    assert returncode == 0, "Should exit successfully"
    assert "Total moves: 3" in output, "Should report 3 moves"
    assert "Move sequence: UP -> LEFT -> UP" in output, "Move sequence should be: UP -> LEFT -> UP"
    assert "Step 1: Move UP" in output, "Should show Step 1: Move UP"
    assert "Step 2: Move LEFT" in output, "Should show Step 2: Move LEFT"
    assert "Step 3: Move UP" in output, "Should show Step 3: Move UP"


def test_four_move_puzzle():
    """Console solver should solve a 4-move puzzle with correct sequence."""
    # Puzzle that's four moves away from solved
    # Solution: LEFT -> UP -> LEFT -> UP
    puzzle_input = "1 2 3 4 5 0 6 8 9 10 7 11 13 14 15 12"

    output, returncode = run_console_solver(puzzle_input)

    assert returncode == 0, "Should exit successfully"
    assert "Total moves: 4" in output, "Should report 4 moves"
    assert "Move sequence: LEFT -> UP -> LEFT -> UP" in output, \
        "Move sequence should be: LEFT -> UP -> LEFT -> UP"
    assert "Step 1: Move LEFT" in output, "Should show Step 1: Move LEFT"
    assert "Step 2: Move UP" in output, "Should show Step 2: Move UP"
    assert "Step 3: Move LEFT" in output, "Should show Step 3: Move LEFT"
    assert "Step 4: Move UP" in output, "Should show Step 4: Move UP"


def test_eight_move_puzzle():
    """Console solver should solve an 8-move puzzle with correct sequence."""
    # Puzzle that's eight moves away from solved (more complex)
    # Solution: DOWN -> DOWN -> LEFT -> LEFT -> UP -> UP -> LEFT -> UP
    puzzle_input = "5 1 2 4 9 6 3 8 0 10 7 11 13 14 15 12"

    output, returncode = run_console_solver(puzzle_input)

    assert returncode == 0, "Should exit successfully"
    assert "Total moves: 8" in output, "Should report 8 moves"
    assert "Move sequence: DOWN -> DOWN -> LEFT -> LEFT -> UP -> UP -> LEFT -> UP" in output, \
        "Move sequence should be: DOWN -> DOWN -> LEFT -> LEFT -> UP -> UP -> LEFT -> UP"
    assert "Step 1: Move DOWN" in output, "Should show Step 1: Move DOWN"
    assert "Step 2: Move DOWN" in output, "Should show Step 2: Move DOWN"
    assert "Step 3: Move LEFT" in output, "Should show Step 3: Move LEFT"
    assert "Step 4: Move LEFT" in output, "Should show Step 4: Move LEFT"
    assert "Step 5: Move UP" in output, "Should show Step 5: Move UP"
    assert "Step 6: Move UP" in output, "Should show Step 6: Move UP"
    assert "Step 7: Move LEFT" in output, "Should show Step 7: Move LEFT"
    assert "Step 8: Move UP" in output, "Should show Step 8: Move UP"


def test_output_contains_board_visualization():
    """Console solver output should include board visualizations."""
    puzzle_input = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15"

    output, returncode = run_console_solver(puzzle_input)

    assert returncode == 0, "Should exit successfully"
    # Should contain board border characters
    assert "+" in output and "-" in output and "|" in output, \
        "Should include board visualization with borders"
    # Should show initial and final states
    assert "Initial puzzle state:" in output, "Should show initial puzzle state"
    assert "PUZZLE SOLVED!" in output, "Should show puzzle solved message"
