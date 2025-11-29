"""
N-Puzzle array representation and operations.

This module provides a flat array representation of square puzzles (9x1 for 3x3, 16x1 for 4x4, 25x1 for 5x5, etc.)
and operations to move the blank space (0) in different directions.
"""

from typing import Optional, Tuple
import math
from functools import lru_cache


TFlat = Tuple[int, ...]
TSquare = Tuple[Tuple[int, ...], ...]


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


def move(state: TFlat, vertical: int, horizontal: int) -> Optional[TFlat]:
    """
    Move the blank space (0) by the specified number of steps.

    Args:
        state: Current puzzle state as flat array
        vertical: Number of steps to move vertically (negative = up, positive = down)
        horizontal: Number of steps to move horizontally (negative = left, positive = right)

    Returns:
        New state with 0 moved, or None if move is invalid

    Examples:
        move(state, -1, 0)  # Move up by 1
        move(state, 1, 0)   # Move down by 1
        move(state, 0, -1)  # Move left by 1
        move(state, 0, 1)   # Move right by 1
        move(state, -2, 3)  # Move up 2 and right 3
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
        return None

    # Calculate new index
    new_index = new_row * size + new_col

    # Create new state by swapping positions
    return tuple(
        state[new_index] if i == zero_index else
        state[zero_index] if i == new_index else
        state[i]
        for i in range(len(state))
    )


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

