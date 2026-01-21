run-frontend:
	cd frontend && npx vite 

run-backend:
	uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --ssl-certfile=certs/192.168.0.108+2.pem --ssl-keyfile=certs/192.168.0.108+2-key.pem --reload

reload-db:
	poetry run python -m backend.api.scripts.reload_db