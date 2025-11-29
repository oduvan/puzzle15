"""
Console-based N-Puzzle solver.

Reads a puzzle state from stdin and displays the solution sequence
with visual board state illustrations at each step.
"""

import sys
import matrix
import calculate

def parse_input(input_line):
    """
    Parse input string into a puzzle state tuple.

    Expects a single line with space-separated numbers representing
    the puzzle tiles row by row (0 represents the blank).
    """
    try:
        tiles = list(map(int, input_line.strip().split()))

        # Determine board size from number of tiles
        board_size = int(len(tiles) ** 0.5)

        if board_size * board_size != len(tiles):
            print("Error: Number of tiles must be a perfect square (e.g., 9, 16, 25)")
            return None, None

        # Validate tiles contain correct numbers
        expected_tiles = set(range(board_size ** 2))
        if set(tiles) != expected_tiles:
            print(f"Error: Tiles must contain numbers 0 to {board_size**2 - 1}")
            return None, None

        # Return as tuple (flat array representation)
        return tuple(tiles), board_size

    except ValueError:
        print("Error: Input must contain only integers separated by spaces")
        return None, None


def print_board(state, board_size):
    """Print a visual representation of the puzzle board."""
    # Calculate column width based on largest number
    max_num = board_size ** 2 - 1
    col_width = len(str(max_num)) + 2

    # Print top border
    print("+" + "-" * (col_width * board_size + board_size - 1) + "+")

    # Print each row
    for i in range(board_size):
        row_str = "|"
        for j in range(board_size):
            tile = state[i * board_size + j]
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
    if direction == (-1, 0):
        return "UP"
    elif direction == (1, 0):
        return "DOWN"
    elif direction == (0, -1):
        return "LEFT"
    elif direction == (0, 1):
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
    state, board_size = parse_input(input_line)
    if state is None:
        return

    print("\nInitial puzzle state:")
    print_board(state, board_size)

    # Check if already solved
    win_state = matrix.get_win(board_size)
    if state == win_state:
        print("\nPuzzle is already solved!")
        return

    # Initialize AI solver
    print(f"\nLoading pattern databases for {board_size}x{board_size} puzzle...")
    try:
        calculate.init(board_size)
    except FileNotFoundError:
        print(f"\nError: Pattern database file 'pattern_db_{board_size}.dat' not found.")
        print(f"Please run 'python3 pattern_db2.py' to build a pattern database for {board_size}x{board_size} puzzles.")
        print(f"Note: The included database is only for 4x4 (15-puzzle).")
        return

    # Solve puzzle
    print("\nSolving puzzle using IDA* algorithm...")
    move_sequence = calculate.ida_star(state)

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
    current_state = state
    for step_num, direction in enumerate(move_sequence, 1):
        # Get the tile number that will move before making the move
        blank_idx = current_state.index(0)
        blank_row = blank_idx // board_size
        blank_col = blank_idx % board_size
        new_blank_row = blank_row + direction[0]
        new_blank_col = blank_col + direction[1]
        new_blank_idx = new_blank_row * board_size + new_blank_col
        tile_number = current_state[new_blank_idx]

        print(f"\nStep {step_num}: Move {direction_to_string(direction)} (tile {tile_number})")
        current_state, _ = matrix.move(current_state, *direction)
        print_board(current_state, board_size)

    # Verify solution
    if current_state == win_state:
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
