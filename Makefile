setup:
	curl -LsSf https://astral.sh/uv/install.sh | sh

api:
	uv sync
	uv run uvicorn source.main:app --reload

streamlit:
	uv sync
	uv run streamlit run app/main.py

run:
	uv sync
	tmux new-session -d -s myapp "uv run uvicorn source.main:app --reload"
	tmux split-window -h "sleep 15 && uv run streamlit run app/main.py"
	tmux attach-session -t myapp
