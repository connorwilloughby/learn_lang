PYTHONPATH=src uv run coverage run -m unittest discover -s tests --duration=2
PYTHONPATH=src uv run coverage report --format=markdown --show-missing
