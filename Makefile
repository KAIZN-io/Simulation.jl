DC_CMD = docker-compose

PHONY = default
default: up

PHONY += up
up:
	$(DC_CMD) up dbWorker simulation server

PHONY += test
test: clean
	$(DC_CMD) up test_webApp
	$(DC_CMD) up test_python
	$(MAKE) up

PHONY += down
down:
	$(DC_CMD) down --remove-orphans

PHONY += clean
clean: down
	$(DC_CMD) down --rmi local --volumes
	rm -rf ./projectQ/server/static
	rm -rf ./node_modules

PHONY += help
help:
	@echo "Makefile for ProjectQ"
	@echo ""
	@echo "default:        -> up"
	@echo "up:             start local development stack."
	@echo "down:           stop all containers and removes them."
	@echo "clean:          stop all containers and removes them, removes images and volumes as well. Removes npm packages. And cleanes up generated files like the web-apps javascript bundle and generated result images."

.DEFAULT:
	@echo "Target not found:" $@
	@echo "Run 'make help' to view available targets."

.PHONY: $(PHONY)

