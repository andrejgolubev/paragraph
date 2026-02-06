run-frontend:
	cd frontend && npx vite 

run-backend:
	uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --ssl-certfile=certs/192.168.0.108+2.pem --ssl-keyfile=certs/192.168.0.108+2-key.pem --reload


up-local: 
	docker compose -f docker-compose-local.yaml up -d --build

down-local: 
	docker compose -f docker-compose-local.yaml down 


up-light: 
	docker compose -f docker-compose-light.yaml up -d --build

down-light: 
	docker compose -f docker-compose-light.yaml down 