"""
Pattern database builder for N-Puzzle solver.

Pre-computes optimal move counts for tile subsets using BFS,
creating lookup tables that serve as admissible heuristics
for the IDA* search algorithm.
"""

import model
import pickle
import sys
from collections import deque
import math
from time import perf_counter_ns
from multiprocessing import Pool

NANO_TO_SEC = 1000000000  # Nanoseconds to seconds conversion

def fact(n):
    """Calculate factorial of n recursively."""
    if n <= 1:
        return 1
    return n * fact(n-1)

def permutations_count(n, r):
    """
    Calculate number of r-permutations of n items (nPr).

    This represents the number of ways to arrange r items
    selected from n total items.
    """
    return math.floor(fact(n)/fact(n-r))

def build_pattern_database(board_size, group, group_number):
    """
    Build a pattern database for a specific tile group using BFS.

    Performs breadth-first search from the solved state, exploring all
    reachable configurations and recording the minimum moves needed to
    solve each pattern. This creates an admissible heuristic.
    """
    # Start from solved state
    puzzle = model.Puzzle(board_size)
    puzzle.count = 0  # Move counter

    # Include blank in group for state exploration
    group_with_blank = group.copy()
    group_with_blank.add(0)

    # BFS data structures
    visited = set()       # States (with blank) already explored
    closed_list = {}      # Pattern states -> minimum move counts
    open_list = deque()   # Queue of states to explore

    # Progress tracking
    iteration = 0
    total_iterations = permutations_count(board_size**2, len(group_with_blank))
    start_time = perf_counter_ns()

    # Initialize BFS from solved state
    # (puzzle state, previous move direction to avoid)
    open_list.append((puzzle,(0,0)))

    while open_list:
        current_puzzle, previous_move = open_list.popleft()

        # Visit this node and record in database
        if not visit_node(current_puzzle,
                         visited,
                         closed_list,
                         group_with_blank,
                         group):
            continue  # Already visited

        # Try all possible moves
        for direction in puzzle.DIRECTIONS:
            # Don't immediately undo the previous move
            if direction == previous_move:
                continue

            is_valid, next_puzzle = current_puzzle.simulateMove(direction)

            if not is_valid:
                continue

            # Increment move count if a tile in our group moved
            if next_puzzle[current_puzzle.blank_position[0]][current_puzzle.blank_position[1]] in group:
                next_puzzle.count += 1

            # Add to queue (with opposite direction to avoid undoing)
            open_list.append((next_puzzle, (-direction[0],-direction[1])))

        iteration += 1

        # Progress reporting
        if iteration % 100000 == 0:
            current_time = perf_counter_ns()
            elapsed_time = (current_time - start_time) / NANO_TO_SEC
            print("Group {}, Iteration {:,} of {:,}, time elapsed: {}".format(group_number, iteration, total_iterations, elapsed_time))
            print("Size of closed list: {:,}".format(len(closed_list)))
            print("Size of open list: {:,}".format(len(open_list)))
            start_time = current_time

    return closed_list


def visit_node(puzzle, visited, closed_list, group_with_blank, group):
    """
    Process a puzzle state during pattern database construction.

    Checks if this state (with blank position) has been visited before.
    If not, records the pattern (without blank) and its move count.
    """
    # Check if we've seen this exact configuration before (including blank)
    puzzle_hash_with_blank = puzzle.hash(group_with_blank)
    if puzzle_hash_with_blank in visited:
        return False  # Already visited

    visited.add(puzzle_hash_with_blank)

    # Record pattern (without blank position) with minimum move count
    group_hash = puzzle.hash(group)
    if group_hash not in closed_list:
        # First time seeing this pattern
        closed_list[group_hash] = puzzle.count
    elif closed_list[group_hash] > puzzle.count:
        # Found a better path to this pattern (shouldn't happen in BFS)
        closed_list[group_hash] = puzzle.count

    return True

def main():
    """
    Build pattern databases for 15-puzzle and save to disk.

    Creates multiple disjoint pattern databases by partitioning
    the tiles into groups. Different partition strategies offer
    trade-offs between database size and heuristic quality.

    Common partitions for 15-puzzle:
    - 663: Groups of 6, 6, and 3 tiles
    - 555: Groups of 5, 5, and 5 tiles (more balanced)
    - 78: Groups of 7 and 8 tiles (larger, stronger heuristic)
    """
    board_size = 4  # 15-puzzle

    # Tile partition: 663 pattern (faster to build)
    #tile_groups = [{1,5,6,9,10,13},{7,8,11,12,14,15},{2,3,4}]

    # Alternative partitions (uncomment to use):
    # 555 pattern (balanced)
    tile_groups = [{1,2,3,4,7},{5,6,9,10,13},{8,11,12,14,15}]

    # 78 pattern (stronger but slower to build)
    #tile_groups = [{1,2,3,4,5,6,7,8},{9,10,11,12,13,14,15}]

    pattern_databases = []

    # Build databases in parallel (one per tile group)
    with Pool(processes=3) as pool:
        results = [pool.apply_async(build_pattern_database, (board_size, tile_groups[i], i)) for i in range(len(tile_groups))]
        results = [res.get() for res in results]

        for res in results:
            pattern_databases.append(res)

    # Save databases to file
    with open('pattern_db_'+str(board_size)+'.dat', 'wb') as pattern_db_file:
        pickle.dump(tile_groups, pattern_db_file)
        pickle.dump(pattern_databases, pattern_db_file)

    # Display statistics
    for i in range(len(pattern_databases)):
        database = pattern_databases[i]
        print("Group:", tile_groups[i], len(database), "permutations")

if __name__ == '__main__':
    # Build pattern databases
    main()
