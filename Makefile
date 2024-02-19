up_build:
	@echo "Building and starting app container ..."
	@docker compose up --build
	@echo "Building and starting app container [OK]"

down:
	@docker compose down

up:
	@echo "down container ..."
	@docker compose down
	@echo "up container ..."
	@docker compose up