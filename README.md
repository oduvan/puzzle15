# NPuzzle

An N-Puzzle solver with both GUI and console interfaces, using IDA* search with pattern database heuristics.

## Quick Start

Use the included Makefile for common tasks:

```bash
make test          # Run all tests
make run           # Start the puzzle solver (interactive)
make pattern_db     # Generate pattern database
make test-easy     # Solve easy puzzle (1 move)
make test-medium   # Solve medium puzzle (8 moves)
make test-hard     # Solve hard puzzle (30 moves)
```


## Console Version

Run `python3 play_console.py` to solve a puzzle from the command line. The program reads a puzzle configuration from stdin and displays the optimal solution sequence with board visualizations at each step.

### Usage
```bash
echo "1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15" | python3 play_console.py
```

The input should be space-separated numbers representing the tiles row by row, where 0 represents the blank space.

Example for a solved 15-puzzle:
```bash
echo "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0" | python3 play_console.py
```

## Pattern Database

Run `python3 pattern_db.py` to rebuild the pattern database file. By default, it will build a 663 partitioned pattern DB for a 15 puzzle on 3 threads. You can modify the board size, partitions, and number of parallel threads in the `pattern_db.py main()` function. The pattern database file included in this git repo is a 555 partition for a 15 puzzle.

### Partition Strategies
- **663**: Groups of 6, 6, and 3 tiles (faster to build)
- **555**: Groups of 5, 5, and 5 tiles (balanced, included in repo)
- **78**: Groups of 7 and 8 tiles (stronger heuristic but slower to build)

## Testing

The project includes end-to-end tests for the console solver.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
```

### Test Suite

The test suite includes 79 tests covering:

- **Puzzle model tests** (43 tests): Core puzzle logic, moves, win conditions, and hashing
- **Calculate module tests** (19 tests): Manhattan distance and heuristic calculations
- **Search function tests** (10 tests): IDA* search algorithm, pruning, and cycle detection
- **End-to-end tests** (7 tests): Console solver with 4x4 puzzles ranging from 1 to 8 moves

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Project Structure

- **`model.py`** - Core puzzle representation and move logic
- **`calculate.py`** - IDA* search algorithm with pattern database heuristics
- **`pattern_db.py`** - Pattern database generation using BFS
- **`play.py`** - GUI interface using pygame
- **`play_console.py`** - Command-line solver interface
- **`tests/`** - Comprehensive test suite (79 tests)
