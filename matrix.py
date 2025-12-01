"""
N-Puzzle array representation and operations.

This module provides a tuple-based flat array representation of square puzzles
(9x1 for 3x3, 16x1 for 4x4, 25x1 for 5x5, etc.) with efficient operations for
puzzle manipulation, heuristic evaluation, and state compression.

Features:
    - Immutable tuple-based state representation (hashable, can be used in sets/dicts)
    - Move operations: move blank tile by arbitrary vertical/horizontal steps
    - Conversion utilities: flat array ↔ square matrix transformations
    - Manhattan distance heuristics for A* search algorithms
    - Compression: pack puzzle states into integers for efficient storage
    - Universal support for any NxN puzzle size
    - LRU caching for performance optimization
"""

from typing import Optional, Tuple
import math
from functools import lru_cache
from bisect import insort


TFlat = Tuple[int, ...]
TSquare = Tuple[Tuple[int, ...], ...]

@lru_cache()
def get_win(size: int) -> TFlat:
    """
    Get the winning position for a square puzzle of given size.

    The winning position is tiles in order: 1, 2, 3, ..., N-1, 0
    where 0 (blank) is in the last position.

    Args:
        size: Size of one dimension of the puzzle (e.g., 3 for 3x3, 4 for 4x4)
    Returns:
        Winning position as flat array
    """
    return tuple(range(1, size * size)) + (0,)


@lru_cache(maxsize=128)
def _get_size_by_length(length: int) -> int:
    """
    Get the size of the square puzzle from the array length.

    Args:
        length: Length of the flat array representation.
    """
    return int(math.sqrt(length))


def get_size(state: TFlat) -> int:
    """
    Get the size of the square puzzle from the array length.

    Args:
        state: Flat array representation of the puzzle

    Returns:
        Size of one dimension (e.g., 4 for a 16-element array)
    """
    return _get_size_by_length(len(state))


def move(state: TFlat, vertical: int, horizontal: int) -> Tuple[Optional[TFlat], Optional[int]]:
    """
    Move the blank space (0) by the specified number of steps.

    Args:
        state: Current puzzle state as flat array
        vertical: Number of steps to move vertically (negative = up, positive = down)
        horizontal: Number of steps to move horizontally (negative = left, positive = right)

    Returns:
        Tuple of (new_state, moved_tile) where moved_tile is the value that moved,
        or (None, None) if move is invalid

    Examples:
        new_state, tile = move(state, -1, 0)  # Move up by 1
        new_state, tile = move(state, 1, 0)   # Move down by 1
        new_state, tile = move(state, 0, -1)  # Move left by 1
        new_state, tile = move(state, 0, 1)   # Move right by 1
        new_state, tile = move(state, -2, 3)  # Move up 2 and right 3
    """
    size = get_size(state)
    zero_index = state.index(0)

    # Get current position
    row = zero_index // size
    col = zero_index % size

    # Calculate new position
    new_row = row + vertical
    new_col = col + horizontal

    # Check if new position is within bounds
    if new_row < 0 or new_row >= size or new_col < 0 or new_col >= size:
        return None, None

    # Calculate new index
    new_index = new_row * size + new_col

    # The tile that will move into the blank position
    moved_tile = state[new_index]

    # Create new state by swapping positions
    new_state = tuple(
        state[new_index] if i == zero_index else
        state[zero_index] if i == new_index else
        state[i]
        for i in range(len(state))
    )

    return (new_state, moved_tile)


def flat_to_square(state: TFlat) -> TSquare:
    """
    Convert flat array representation to 2D matrix.

    Args:
        state: Puzzle state as flat array

    Returns:
        NxN matrix representation
    """
    size = get_size(state)
    return tuple(state[i * size:(i + 1) * size] for i in range(size))


def square_to_flat(matrix: TSquare) -> TFlat:
    """
    Convert 2D matrix representation to flat array.

    Args:
        matrix: NxN matrix representation

    Returns:
        Flat array representation
    """
    return tuple(item for row in matrix for item in row)


def replace_with_zeros(state: TFlat, tiles_to_keep: set) -> TFlat:
    """
    Keep only specified tiles, replace everything else with zeros.

    This is useful for pattern database calculations where you want to
    focus only on specific tiles and ignore all others.

    Args:
        state: Puzzle state as flat array
        tiles_to_keep: Set of tile values to keep (all others become 0)

    Returns:
        New state with only specified tiles kept, rest replaced by 0

    Example:
        state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        result = replace_with_zeros(state, {1, 2, 5, 8})
        # result = (1, 2, 0, 0, 5, 0, 0, 8, 0)
    """
    return tuple(tile if tile in tiles_to_keep else 0 for tile in state)


def manhattan_distance(current: TFlat, goal: TFlat) -> int:
    """
    Calculate the Manhattan distance heuristic between current and goal states.

    Manhattan distance is the sum of horizontal and vertical distances
    each tile must travel to reach its goal position.

    Args:
        current: Current puzzle state as flat array
        goal: Goal/desired puzzle state as flat array

    Returns:
        Total Manhattan distance (sum for all tiles except blank/0)

    Example:
        current = (1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 7, 12, 13, 14, 11, 15)
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
        manhattan_distance(current, goal) = 6
    """
    size = get_size(current)
    distance = 0

    for i, tile in enumerate(current):
        if not tile:  # Skip the blank tile
            continue

        current_row = i // size
        current_col = i % size

        goal_index = goal.index(tile)
        goal_row = goal_index // size
        goal_col = goal_index % size

        distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return distance


def manhattan_distance_to_win(current: TFlat) -> int:
    """
    Calculate the Manhattan distance to the standard winning position.

    The winning position is tiles in order: 1, 2, 3, ..., N-1, 0
    where 0 (blank) is in the last position.

    This is optimized compared to manhattan_distance() because it doesn't
    need to look up goal positions - they can be calculated directly.

    Args:
        current: Current puzzle state as flat array

    Returns:
        Total Manhattan distance to winning position (sum for all tiles except blank/0)

    Example:
        For 3x3: winning = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        For 4x4: winning = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    """
    size = get_size(current)
    distance = 0

    for i, tile in enumerate(current):
        if not tile:  # Skip the blank tile
            continue

        current_row = i // size
        current_col = i % size

        # In winning position, tile N is at index N-1
        goal_index = tile - 1
        goal_row = goal_index // size
        goal_col = goal_index % size

        distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return distance


def is_solvable(state: TFlat) -> bool:
    """
    Check if a puzzle configuration is solvable using incremental sorted list approach.

    This algorithm builds a sorted list incrementally while scanning tiles, computing
    a parity sum based on inversions and blank position. For each tile, the index in
    the sorted list gives the count of previously seen smaller tiles, which indirectly
    counts inversions. The blank's row is added to account for position parity.

    For the 15-puzzle (4x4) and other NxN puzzles where N is even:
    - Solvable if parity sum is EVEN

    For 3x3 and other NxN puzzles where N is odd:
    - Solvable if parity sum is EVEN

    Args:
        state: Puzzle state as flat array

    Returns:
        True if solvable, False if unsolvable

    Example:
        For 4x4 (15-puzzle):
        state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0)
        is_solvable(state)  # False (unsolvable - tiles 14 and 15 swapped)
    """
    size = get_size(state)
    p = []
    s = 0

    for i in range(len(state)):
        x = state[i]
        row = i // size

        if x == 0:
            s += row  # Add row index for blank
        else:
            insort(p, x)
            s += p.index(x)

    return not s % 2  # Solvable if sum is EVEN


@lru_cache()
def _compress_attributes(size: int) -> int:
    """
    Calculate and cache the number of bits needed per value for a given puzzle size.

    This is cached to avoid recalculating for the same puzzle size.

    Args:
        size: Size of one dimension of the puzzle (e.g., 3 for 3x3, 4 for 4x4)

    Returns:
        Number of bits required to represent any value in the puzzle.
        For example: 3x3 needs 4 bits (max value 8), 5x5 needs 5 bits (max value 24).
    """
    return (size * size - 1).bit_length()


def compress(state: TFlat) -> int:
    """
    Compress a puzzle state into a single integer.

    This packs all tile values into bits for efficient storage.
    Each value uses the minimum number of bits needed (e.g., 4 bits for 3x3/4x4, 5 bits for 5x5).

    Args:
        state: Puzzle state as flat array

    Returns:
        Compressed integer representation

    Example:
        state = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 3x3
        compressed = compress(state)  # Returns integer with all values packed
    """
    size = get_size(state)
    bits_per_value = _compress_attributes(size)
    result = 0
    for val in state:
        result = (result << bits_per_value) | val
    return result


@lru_cache()
def _decompress_attributes(size: int) -> Tuple[int, Tuple[int, ...]]:
    """
    Calculate and cache decompression parameters for a given puzzle size.

    This precomputes the bit mask and shift amounts needed to extract each value
    from the compressed integer, avoiding redundant calculations.

    Args:
        size: Size of one dimension of the puzzle (e.g., 3 for 3x3, 4 for 4x4)

    Returns:
        Tuple of (mask, shifts) where:
        - mask: Bit mask to extract a single value (e.g., 0xF for 4 bits)
        - shifts: Tuple of bit shift amounts for each position in the puzzle
    """
    length = size * size
    bits_per_value = _compress_attributes(size)
    mask = (1 << bits_per_value) - 1
    shifts = tuple((length - 1 - i) * bits_per_value for i in range(length))
    return mask, shifts


def decompress(n: int, size: int) -> TFlat:
    """
    Decompress an integer back into a puzzle state.

    Args:
        n: Compressed integer representation
        size: Size of one dimension of the puzzle (e.g., 3 for 3x3, 4 for 4x4)

    Returns:
        Puzzle state as flat array

    Example:
        compressed = 12345678
        state = decompress(compressed, 3)  # Returns 3x3 puzzle state
    """
    mask, shifts = _decompress_attributes(size)

    values = []
    for shift in shifts:
        val = (n >> shift) & mask
        values.append(val)
    return tuple(values)


# Move encoding constants (2 bits per move)
_MOVE_UP = 0b00      # (-1, 0)
_MOVE_DOWN = 0b01    # (1, 0)
_MOVE_LEFT = 0b10    # (0, -1)
_MOVE_RIGHT = 0b11   # (0, 1)

_MOVE_TO_CODE = {
    (-1, 0): _MOVE_UP,
    (1, 0): _MOVE_DOWN,
    (0, -1): _MOVE_LEFT,
    (0, 1): _MOVE_RIGHT,
}

_CODE_TO_MOVE = {
    _MOVE_UP: (-1, 0),
    _MOVE_DOWN: (1, 0),
    _MOVE_LEFT: (0, -1),
    _MOVE_RIGHT: (0, 1),
}


def compress_moves(moves: list) -> int:
    """
    Compress a sequence of moves into a single integer with length embedded.

    Format: [Lower 8 bits: length][Higher bits: compressed moves]
    Each move is encoded as 2 bits:
    - Up (-1, 0): 00
    - Down (1, 0): 01
    - Left (0, -1): 10
    - Right (0, 1): 11

    Args:
        moves: List of move tuples, e.g., [(-1, 0), (0, 1), (1, 0)]

    Returns:
        Compressed integer with length and moves packed

    Example:
        moves = [(-1, 0), (1, 0), (0, -1)]  # up, down, left
        compressed = compress_moves(moves)
        # Lower 8 bits: 3 (length)
        # Higher bits: 0b00_01_10 (moves)
    """
    length = len(moves)
    compressed_moves = 0
    for move in moves:
        code = _MOVE_TO_CODE[move]
        compressed_moves = (compressed_moves << 2) | code
    # Pack: moves in higher bits, length in lower 8 bits
    return (compressed_moves << 8) | length


def decompress_moves(packed: int) -> list:
    """
    Decompress an integer back into a sequence of moves.

    Args:
        packed: Packed integer with length in lower 8 bits and moves in higher bits

    Returns:
        List of move tuples

    Example:
        packed = compress_moves([(-1, 0), (1, 0), (0, -1)])
        moves = decompress_moves(packed)  # [(-1, 0), (1, 0), (0, -1)]
    """
    # Extract length from lower 8 bits
    length = packed & 0xFF
    # Extract compressed moves from higher bits
    compressed_moves = packed >> 8

    moves = []
    mask = 0b11  # 2 bits
    for i in range(length):
        shift = (length - 1 - i) * 2
        code = (compressed_moves >> shift) & mask
        moves.append(_CODE_TO_MOVE[code])
    return moves


def get_moves_length(packed: int) -> int:
    """
    Extract the length of a compressed move sequence without decompressing.

    This is more efficient than decompressing when you only need the count.

    Args:
        packed: Packed integer with length in lower 8 bits and moves in higher bits

    Returns:
        Number of moves in the sequence

    Example:
        packed = compress_moves([(-1, 0), (1, 0), (0, -1)])
        length = get_moves_length(packed)  # 3
    """
    return packed & 0xFF

