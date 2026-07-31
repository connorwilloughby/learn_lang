uv run ruff format 
uv run ruff check --fix 
PYTHONPATH=src uv run -m unittest discover -s tests 