.PHONY: test test-cov diff-cov lint type-check check

test:
	uv run python -m pytest tests/unit/ -v

test-cov:
	uv run python -m pytest tests/unit/ -v \
		--cov --cov-branch \
		--cov-report=term-missing \
		--cov-report=html:htmlcov \
		--cov-report=xml:coverage.xml

diff-cov: test-cov
	uv run diff-cover coverage.xml --compare-branch=origin/main --fail-under=90

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

type-check:
	uv run mypy src/

check: lint type-check test-cov
