import pickle
import time
from collections import deque

import matrix

# Tile partition: 663 pattern (faster to build)
#TILE_GROUPS = [{1,5,6,9,10,13},{7,8,11,12,14,15},{2,3,4}]

# Alternative partitions (uncomment to use):
# 555 pattern (balanced)
TILE_GROUPS = [{1,2,3,4,7},{5,6,9,10,13},{8,11,12,14,15}]

# 78 pattern (stronger but slower to build)
#TILE_GROUPS = [{1,2,3,4,5,6,7,8},{9,10,11,12,13,14,15}]

SIZE = 4  # 15-puzzle

DIRECTIONS = [(1,0),(-1,0),(0,1),(0,-1)]

pattern_databases = []
total_start_time = time.time()

# Build pattern database for each group sequentially
for group_idx, tile_group in enumerate(TILE_GROUPS):
    print(f"\nBuilding pattern database for group {group_idx + 1}/{len(TILE_GROUPS)}: {tile_group}")

    pattern_db = {}
    open_list = deque()
    visited = set()
    # Track group tiles + blank for visited check
    tile_group_with_blank = sorted(tile_group | {0})

    # Initialize solved state with cost 0
    solved_state = matrix.get_win(SIZE)
    tile_group_puzzle = matrix.replace_with_zeros(solved_state, tile_group)
    puzzle_key = matrix.compress(tile_group_puzzle)
    pattern_db[puzzle_key] = 0

    open_list.append((solved_state, 0, (0, 0)))  # (puzzle, move_count, last_direction)

    iteration = 0
    start_time = time.time()

    while open_list:
        puzzle, move_count, last_direction = open_list.popleft()

        if iteration and iteration % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"{elapsed:.1f}s; {iteration:,}: depth - {move_count}, queue - {len(open_list):,}, visited - {len(visited):,}, patterns - {len(pattern_db):,}")
        iteration += 1

        for direction in DIRECTIONS:
            # Skip reverse move (avoid tuple creation)
            if direction[0] == -last_direction[0] and direction[1] == -last_direction[1]:
                continue

            new_puzzle, tile = matrix.move(puzzle, *direction)
            if new_puzzle is None:
                continue

            # Create visited key from positions of group tiles + blank
            # This tracks WHERE these tiles are, not just their values
            positions = tuple(new_puzzle.index(t) for t in tile_group_with_blank)
            if positions in visited:
                continue

            visited.add(positions)

            # Check if moved tile is in current group
            if tile in tile_group:
                # Tile in our group - increment count
                new_count = move_count + 1

                # Record pattern if new or improved
                tile_group_puzzle = matrix.replace_with_zeros(new_puzzle, tile_group)
                puzzle_key = matrix.compress(tile_group_puzzle)

                if pattern_db.get(puzzle_key, float('inf')) > new_count:
                    pattern_db[puzzle_key] = new_count

                # Always explore (might lead to other patterns)
                open_list.append((new_puzzle, new_count, direction))
            else:
                # Tile not in our group - don't increment count, still explore
                open_list.append((new_puzzle, move_count, direction))

    elapsed = time.time() - start_time
    print(f"Group {group_idx + 1} complete: {len(pattern_db):,} patterns in {elapsed:.1f}s")
    pattern_databases.append(pattern_db)

total_elapsed = time.time() - total_start_time
print(f"\nTotal time: {total_elapsed:.1f}s")
print(f"Total patterns: {sum(len(db) for db in pattern_databases):,}")

with open('pattern_db_'+str(SIZE)+'.dat', 'wb') as pattern_db_file:
    pickle.dump(TILE_GROUPS, pattern_db_file)
    pickle.dump(pattern_databases, pattern_db_file)
