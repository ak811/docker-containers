COMPOSE=docker compose

build:
	$(COMPOSE) build app db

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down -v

clean: down
	rm -rf out && mkdir -p out

all: clean up
