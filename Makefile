all:
	uv sync
	uv run uvicorn app.main:app --reload
# 	uv run -m app.main

#TODO install uv
