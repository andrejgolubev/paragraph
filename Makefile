run-frontend:
	cd frontend && npx vite 

run-backend:
	cd api && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload