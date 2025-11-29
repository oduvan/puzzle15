"""
IDA* (Iterative Deepening A*) solver for N-Puzzle.

This module implements an optimal solver using IDA* search with
pattern database heuristics for efficient solution finding.
"""

import pickle

# Constants
INFINITY = 100000  # Represents unreachable cost in search

# Global pattern database storage
pattern_groups = []      # List of tile groups for each pattern database
pattern_databases = []   # List of dictionaries mapping puzzle states to move counts

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

def ida_star(puzzle):
    """
    Solve the puzzle using IDA* (Iterative Deepening A*) algorithm.

    IDA* performs depth-first searches with increasing cost thresholds,
    combining the space efficiency of depth-first search with the
    optimality guarantees of A*.
    """
    # Already solved
    if puzzle.checkWin():
        return []

    # Load pattern database if not already loaded
    if not pattern_databases:
        init(puzzle.boardSize)

    # Initial cost threshold is the heuristic estimate
    bound = calculate_heuristic(puzzle)
    path = [puzzle]  # Path of puzzle states explored
    move_sequence = []  # Sequence of moves to reach current state
    import pdb; pdb.set_trace()
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
    current_puzzle = path[-1]
    # f(n) = g(n) + h(n): actual cost + heuristic estimate
    cost = depth + calculate_heuristic(current_puzzle)

    # Prune if exceeds current bound
    if cost > bound:
        return cost

    # Goal test
    if current_puzzle.checkWin():
        return True

    minimum_cost = INFINITY

    # Try all possible moves
    for direction in current_puzzle.DIRECTIONS:
        # Don't undo the previous move (optimization)
        if move_sequence and (-direction[0], -direction[1]) == move_sequence[-1]:
            continue

        is_valid, next_puzzle = current_puzzle.simulateMove(direction)

        # Skip invalid moves and cycles (revisiting states)
        if not is_valid or next_puzzle in path:
            continue

        # Explore this branch
        path.append(next_puzzle)
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

def calculate_manhattan_distance(puzzle, group):
    """
    Calculate Manhattan distance heuristic for a group of tiles.

    Manhattan distance is the sum of horizontal and vertical distances
    each tile must travel to reach its goal position.
    """
    distance = 0
    for i in range(puzzle.boardSize):
        for j in range(puzzle.boardSize):
            if puzzle[i][j] != 0 and puzzle[i][j] in group:
                # Calculate where this tile should be
                destination_position = ((puzzle[i][j] - 1) // puzzle.boardSize,
                                        (puzzle[i][j] - 1) % puzzle.boardSize)
                # Add Manhattan distance
                distance += abs(destination_position[0] - i)
                distance += abs(destination_position[1] - j)
    return distance

def calculate_heuristic(puzzle):
    """
    Calculate heuristic estimate using pattern databases.

    The heuristic is the sum of optimal move counts for each tile group
    from the pattern databases. This is admissible (never overestimates)
    because each group can be solved independently in at least that many moves.
    """
    heuristic_value = 0

    # Sum heuristics from all pattern databases
    for group_index, group in enumerate(pattern_groups):
        # Generate hash for this group's tile positions
        group_hash = puzzle.hash(group)

        if group_hash in pattern_databases[group_index]:
            # Look up pre-computed optimal move count for this pattern
            heuristic_value += pattern_databases[group_index][group_hash]
        else:
            # Fallback to Manhattan distance if pattern not in database
            print("No pattern found in DB, using manhattan distance")
            heuristic_value += calculate_manhattan_distance(puzzle, group)

    return heuristic_value
