dev:
	docker-compose up -d

dev-down:
	docker-compose down

push-migration:
	alembic upgrade head

start-server:
	uvicorn src.main:app --reload

install-modules:
	pip install fastapi[all] fastapi-mail==1.2.2 fastapi-jwt-auth[asymmetric] passlib[bcrypt] alembic SQLAlchemy psycopg2