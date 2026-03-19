run-frontend:
	cd frontend && npx vite 

run-backend:
	uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --ssl-certfile=certs/localhost+2.pem --ssl-keyfile=certs/localhost+2-key.pem --reload


up-local: 
	docker compose -f docker-compose-local.yaml up -d --build

down-local: 
	docker compose -f docker-compose-local.yaml down 


up-lite: 
	docker compose -f docker-compose-lite.yaml up -d --build

down-lite: 
	docker compose -f docker-compose-lite.yaml down 


up-test: 
	docker compose -f docker-compose-test.yaml up -d --build

down-test: 
	docker compose -f docker-compose-test.yaml down 