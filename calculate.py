"""
IDA* (Iterative Deepening A*) solver for N-Puzzle.

This module implements an optimal solver using IDA* search with
pattern database heuristics for efficient solution finding.
"""

import pickle
import matrix

# Constants
INFINITY = 100000  # Represents unreachable cost in search

# Global pattern database storage
pattern_groups = []      # List of tile groups for each pattern database
pattern_databases = []   # List of dictionaries mapping puzzle states to move counts
DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]  # Down, Up, Right, Left

def init(boardSize):
    """
    Load pre-computed pattern databases from disk.

    Pattern databases contain pre-computed optimal move counts for
    subsets of tiles, used as heuristics in the IDA* search.
    """
    global pattern_groups
    global pattern_databases
    print("Initializing pattern DB...")
    with open("pattern_db_"+str(boardSize)+".dat", "rb") as pattern_db_file:
        # Load tile groups and their corresponding databases
        pattern_groups = pickle.load(pattern_db_file)
        pattern_databases = pickle.load(pattern_db_file)
        # Display loaded database statistics
        for i in range(len(pattern_databases)):
            print("Group {}: {}, {:,} entries.".format(i, pattern_groups[i], len(pattern_databases[i])))

def ida_star(state):
    """
    Solve the puzzle using IDA* (Iterative Deepening A*) algorithm.

    IDA* performs depth-first searches with increasing cost thresholds,
    combining the space efficiency of depth-first search with the
    optimality guarantees of A*.

    Args:
        state: Puzzle state as flat tuple

    Returns:
        List of direction tuples representing the solution moves
    """
    # Check if already solved
    board_size = matrix.get_size(state)
    win_state = matrix.get_win(board_size)
    if state == win_state:
        return []

    # Load pattern database if not already loaded
    if not pattern_databases:
        init(board_size)

    # Initial cost threshold is the heuristic estimate
    bound = calculate_heuristic(state)
    path = [state]  # Path of puzzle states explored
    move_sequence = []  # Sequence of moves to reach current state

    while True:
        # Search with current bound
        result = search(path, 0, bound, move_sequence)

        if result == True:
            return move_sequence
        elif result == INFINITY:
            # No solution exists
            return None

        # Increase bound to minimum exceeded value and retry
        print("Increasing bound to:", result, "From:", bound)
        bound = result

def search(path, depth, bound, move_sequence):
    """
    Recursive depth-first search with cost threshold.

    This is the core of IDA*, exploring paths depth-first while
    pruning branches that exceed the current cost threshold.
    """
    current_state = path[-1]
    # f(n) = g(n) + h(n): actual cost + heuristic estimate
    cost = depth + calculate_heuristic(current_state)

    # Prune if exceeds current bound
    if cost > bound:
        return cost

    # Goal test
    board_size = matrix.get_size(current_state)
    win_state = matrix.get_win(board_size)
    if current_state == win_state:
        return True

    minimum_cost = INFINITY

    # Try all possible moves
    for direction in DIRECTIONS:
        # Don't undo the previous move (optimization)
        if move_sequence and (-direction[0], -direction[1]) == move_sequence[-1]:
            continue

        next_state, _ = matrix.move(current_state, *direction)

        # Skip invalid moves and cycles (revisiting states)
        if next_state is None or next_state in path:
            continue

        # Explore this branch
        path.append(next_state)
        move_sequence.append(direction)

        search_result = search(path, depth + 1, bound, move_sequence)

        if search_result == True:
            return True  # Solution found

        # Track minimum cost that exceeded bound (for next iteration)
        if search_result < minimum_cost:
            minimum_cost = search_result

        # Backtrack
        path.pop()
        move_sequence.pop()

    return minimum_cost

def calculate_heuristic(state):
    """
    Calculate heuristic estimate using pattern databases.

    The heuristic is the sum of optimal move counts for each tile group
    from the pattern databases. This is admissible (never overestimates)
    because each group can be solved independently in at least that many moves.

    Args:
        state: Puzzle state as flat tuple

    Returns:
        Heuristic value (estimated cost to goal)
    """
    heuristic_value = 0

    # Sum heuristics from all pattern databases
    for group_index, group in enumerate(pattern_groups):
        # Create pattern: keep only tiles in this group, zero out others
        pattern_state = matrix.replace_with_zeros(state, group)
        group_hash = matrix.compress(pattern_state)

        if group_hash in pattern_databases[group_index]:
            # Look up pre-computed optimal move count for this pattern
            heuristic_value += pattern_databases[group_index][group_hash]
        else:
            # Fallback to Manhattan distance if pattern not in database
            print(f"No pattern found in DB for group {group}, using manhattan distance")
            pattern_state_for_md = matrix.replace_with_zeros(state, group)
            heuristic_value += matrix.manhattan_distance_to_win(pattern_state_for_md)

    return heuristic_value
