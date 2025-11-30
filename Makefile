.PHONY: help test run pattern_db test-easy test-medium test-hard clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make test         - Run all tests"
	@echo "  make run          - Start the puzzle solver (interactive)"
	@echo "  make pattern_db    - Generate pattern database"
	@echo ""
	@echo "Predefined puzzle tests:"
	@echo "  make test-easy    - Solve easy puzzle (1 move)"
	@echo "  make test-medium  - Solve medium puzzle (8 moves)"
	@echo "  make test-hard    - Solve hard puzzle (30 moves)"
	@echo ""
	@echo "  make clean        - Remove Python cache files"

# Run all tests
test:
	python3 -m pytest -v

# Start the puzzle solver client
run:
	python3 play_console.py

run-no-frontier:
	python3 play_console.py --no-frontier

# Generate pattern database
pattern_db:
	python3 pattern_db.py

# Predefined puzzle tests
test-easy:
	@echo "Testing easy puzzle (1 move)..."
	@echo "1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15" | python3 play_console.py

test-medium:
	@echo "Testing medium puzzle (8 moves)..."
	@echo "5 1 2 4 9 6 3 8 0 10 7 11 13 14 15 12" | python3 play_console.py
