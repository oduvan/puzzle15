"""
Console-based N-Puzzle solver.

Reads a puzzle state from stdin and displays the solution sequence
with visual board state illustrations at each step.
"""

import sys
import model
import calculate

def parse_input(input_line):
    """
    Parse input string into a puzzle board.

    Expects a single line with space-separated numbers representing
    the puzzle tiles row by row (0 represents the blank).
    """
    try:
        tiles = list(map(int, input_line.strip().split()))

        # Determine board size from number of tiles
        board_size = int(len(tiles) ** 0.5)

        if board_size * board_size != len(tiles):
            print("Error: Number of tiles must be a perfect square (e.g., 9, 16, 25)")
            return None

        # Validate tiles contain correct numbers
        expected_tiles = set(range(board_size ** 2))
        if set(tiles) != expected_tiles:
            print(f"Error: Tiles must contain numbers 0 to {board_size**2 - 1}")
            return None

        # Create puzzle
        puzzle = model.Puzzle(board_size)

        # Set board configuration from input
        for i in range(board_size):
            for j in range(board_size):
                tile_value = tiles[i * board_size + j]
                puzzle.board[i][j] = tile_value
                if tile_value == 0:
                    puzzle.blank_position = (i, j)

        return puzzle

    except ValueError:
        print("Error: Input must contain only integers separated by spaces")
        return None


def print_board(puzzle):
    """Print a visual representation of the puzzle board."""
    board_size = puzzle.boardSize

    # Calculate column width based on largest number
    max_num = board_size ** 2 - 1
    col_width = len(str(max_num)) + 2

    # Print top border
    print("+" + "-" * (col_width * board_size + board_size - 1) + "+")

    # Print each row
    for i in range(board_size):
        row_str = "|"
        for j in range(board_size):
            tile = puzzle.board[i][j]
            if tile == 0:
                # Blank tile
                row_str += " " * col_width
            else:
                # Number tile, centered
                tile_str = str(tile)
                padding = col_width - len(tile_str)
                left_pad = padding // 2
                right_pad = padding - left_pad
                row_str += " " * left_pad + tile_str + " " * right_pad

            if j < board_size - 1:
                row_str += "|"
        row_str += "|"
        print(row_str)

        # Print row separator (except after last row)
        if i < board_size - 1:
            print("|" + "-" * (col_width * board_size + board_size - 1) + "|")

    # Print bottom border
    print("+" + "-" * (col_width * board_size + board_size - 1) + "+")


def direction_to_string(direction):
    """Convert direction tuple to readable string."""
    if direction == model.Puzzle.UP:
        return "UP"
    elif direction == model.Puzzle.DOWN:
        return "DOWN"
    elif direction == model.Puzzle.LEFT:
        return "LEFT"
    elif direction == model.Puzzle.RIGHT:
        return "RIGHT"
    else:
        return "UNKNOWN"


def main():
    """
    Main function for console puzzle solver.

    Reads puzzle from stdin, solves it using IDA*, and displays
    the solution sequence with board visualizations.
    """
    print("N-Puzzle Console Solver")
    print("=" * 50)
    print()
    print("Enter puzzle as space-separated numbers (0 = blank):")
    print("Example for 15-puzzle: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15")
    print()

    # Read input
    input_line = sys.stdin.readline()

    # Parse puzzle
    puzzle = parse_input(input_line)
    if puzzle is None:
        return

    print("\nInitial puzzle state:")
    print_board(puzzle)

    # Check if already solved
    if puzzle.checkWin():
        print("\nPuzzle is already solved!")
        return

    # Initialize AI solver
    print(f"\nLoading pattern databases for {puzzle.boardSize}x{puzzle.boardSize} puzzle...")
    try:
        calculate.init(puzzle.boardSize)
    except FileNotFoundError:
        print(f"\nError: Pattern database file 'pattern_db_{puzzle.boardSize}.dat' not found.")
        print(f"Please run 'python3 pattern_db.py' to build a pattern database for {puzzle.boardSize}x{puzzle.boardSize} puzzles.")
        print(f"Note: The included database is only for 4x4 (15-puzzle).")
        return

    # Solve puzzle
    print("\nSolving puzzle using IDA* algorithm...")
    move_sequence = calculate.ida_star(puzzle)

    if move_sequence is None:
        print("\nNo solution found! The puzzle may be unsolvable.")
        return

    if len(move_sequence) == 0:
        print("\nPuzzle is already solved!")
        return

    # Display solution
    print(f"\nSolution found with {len(move_sequence)} moves!")
    print("\n" + "=" * 50)
    print("SOLUTION SEQUENCE")
    print("=" * 50)

    # Show each step
    for step_num, direction in enumerate(move_sequence, 1):
        # Get the tile number that will move before making the move
        new_blank_row = puzzle.blank_position[0] + direction[0]
        new_blank_col = puzzle.blank_position[1] + direction[1]
        tile_number = puzzle.board[new_blank_row][new_blank_col]

        print(f"\nStep {step_num}: Move {direction_to_string(direction)} (tile {tile_number})")
        puzzle.move(direction)
        print_board(puzzle)

    # Verify solution
    if puzzle.checkWin():
        print("\n" + "=" * 50)
        print("PUZZLE SOLVED!")
        print("=" * 50)
    else:
        print("\nWarning: Final state is not solved (this shouldn't happen)")

    # Print move summary
    print(f"\nTotal moves: {len(move_sequence)}")
    print("Move sequence: " + " -> ".join([direction_to_string(d) for d in move_sequence]))


if __name__ == "__main__":
    main()
