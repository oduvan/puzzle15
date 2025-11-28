"""
N-Puzzle game model.

This module implements the core puzzle logic for sliding tile puzzles
(e.g., 8-puzzle, 15-puzzle, 24-puzzle).
"""

from copy import deepcopy

# Predefined winning positions for common board sizes
WINNING_BOARDS = {
    3: [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
    4: [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]],
    5: [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 0]]
}

class Puzzle:
    """
    Represents an N-puzzle sliding tile game.

    The puzzle consists of a square board with numbered tiles and one blank space.
    Tiles adjacent to the blank can slide into the blank position.
    """

    # Direction vectors for moving the blank tile (row_delta, col_delta)
    UP = (1,0)     # Move blank down (tile moves up)
    DOWN = (-1,0)  # Move blank up (tile moves down)
    LEFT = (0,1)   # Move blank right (tile moves left)
    RIGHT = (0,-1) # Move blank left (tile moves right)

    DIRECTIONS = [UP,DOWN,LEFT,RIGHT]

    def __init__(self, boardSize = 4):
        """Initialize a new puzzle in solved state."""
        self.boardSize = boardSize
        # Initialize board with zeros
        self.board = [[0]*boardSize for i in range(boardSize)]
        # Blank starts at bottom-right corner
        self.blank_position = (boardSize-1, boardSize-1)

        # Fill board with numbers 1 to boardSize^2 - 1 in order
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j] = i * boardSize + j + 1

        # Set blank square (0) in bottom right corner - this is the solved state
        self.board[self.blank_position[0]][self.blank_position[1]] = 0

    def __str__(self):
        """Return a string representation of the puzzle board."""
        output_string = ''
        for i in self.board:
            output_string += '\t'.join(map(str,i))
            output_string += '\n'
        return output_string

    def __getitem__(self, key):
        """Allow indexing into the puzzle like puzzle[row][col]."""
        return self.board[key]

    def move(self, direction):
        """Move the blank tile in the given direction."""
        # Calculate where the blank would move to
        new_blank_position = (self.blank_position[0] + direction[0], self.blank_position[1] + direction[1])

        # Check if the new position is within board bounds
        if new_blank_position[0] < 0 or new_blank_position[0] >= self.boardSize \
            or new_blank_position[1] < 0 or new_blank_position[1] >= self.boardSize:
            return False

        # Swap the blank with the tile in the target position
        self.board[self.blank_position[0]][self.blank_position[1]] = self.board[new_blank_position[0]][new_blank_position[1]]
        self.board[new_blank_position[0]][new_blank_position[1]] = 0
        self.blank_position = new_blank_position
        return True


    def checkWin(self):
        """
        Check if the puzzle is in the solved state.

        The solved state has tiles numbered 1 to boardSize^2-1 in order,
        with the blank (0) in the bottom-right corner.
        """
        # Use predefined winning board if available
        if self.boardSize in WINNING_BOARDS:
            return self.board == WINNING_BOARDS[self.boardSize]

        # Fallback for uncommon board sizes
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] != i * self.boardSize + j + 1 and self.board[i][j] != 0:
                    return False
        return True

    def hash(self, group = {}):
        """
        Generate a hash string representing the positions of tiles in a group.

        Used by the pattern database to identify puzzle states based on
        specific tile positions (ignoring other tiles).
        """
        if not group:
            group = {s for s in range(self.boardSize**2)}

        # Create string with position of each tile (row, col pairs)
        hash_string = ['0']*2*(self.boardSize**2)

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self[i][j] in group:
                    # Store row and column for tiles in the group
                    hash_string[2*self[i][j]] = str(i)
                    hash_string[2*self[i][j]+1] = str(j)
                else:
                    # Mark tiles not in group with 'x' (removed later)
                    hash_string[2*self[i][j]] = 'x'
                    hash_string[2*self[i][j]+1] = 'x'

        # Join and remove positions of tiles not in group
        return ''.join(hash_string).replace('x','')
    def simulateMove(self, direction):
        """
        Simulate a move without modifying the current puzzle state.

        Creates a deep copy of the puzzle and attempts the move on the copy.
        Useful for search algorithms that need to explore possibilities.
        """
        simulated_puzzle = deepcopy(self)

        return simulated_puzzle.move(direction), simulated_puzzle
