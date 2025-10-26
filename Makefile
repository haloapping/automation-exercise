format:
	ruff format

check:
	ruff check

test:
	@echo "Running tests in sequential..."
	python3 -m pytest tests/ -s -v --html=report.html --self-contained-html

testp:
	@echo "Running tests in parallel..."
	python3 -m pytest tests/ -n auto -s -v --html=report.html --self-contained-html