
.PHONY: setup-backend run-backend setup-frontend run-frontend run-front-root run-all test clean

# Backend: create venv and install requirements
setup-backend:
	python3 -m venv backend/.venv
	backend/.venv/bin/python -m pip install --upgrade pip
	backend/.venv/bin/pip install -r backend/requirements.txt

# Run the backend (uses uvicorn from the backend venv)
run-backend:
	backend/.venv/bin/uvicorn --app-dir backend app.main:app --reload --port 8000

# Frontend (folder): create venv and install requirements
setup-frontend:
	python3 -m venv frontend/.venv
	frontend/.venv/bin/python -m pip install --upgrade pip
	frontend/.venv/bin/pip install -r frontend/requirements.txt

# Run the frontend that lives in frontend/
run-frontend:
	frontend/.venv/bin/streamlit run frontend/streamlit_app.py

# Run the root-level Streamlit app (streamlit_app.py at repo root)
run-front-root:
	python3 -m venv .venv || true
	. .venv/bin/activate && pip install -r frontend/requirements.txt && .venv/bin/streamlit run streamlit_app.py

# Start backend in background and then frontend in foreground (both from venvs)
run-all: setup-backend setup-frontend
	@echo "Starting backend in background and frontend in foreground"
	@backend/.venv/bin/uvicorn --app-dir backend app.main:app --reload --port 8000 & frontend/.venv/bin/streamlit run frontend/streamlit_app.py

# Run backend tests (if tests are added under backend/)
test: setup-backend
	backend/.venv/bin/pytest -q

clean:
	rm -rf backend/.venv frontend/.venv .venv

