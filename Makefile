DC_CMD = docker-compose

PHONY = default
default: up

PHONY += up
up:
	$(DC_CMD) up persistor py_simulator server

PHONY += py_up
julia_up:
	$(DC_CMD) up -d bundler persistor julia_simulator
	$(DC_CMD) up -d --no-deps server
	$(DC_CMD) logs -f persistor julia_simulator server

PHONY += build
build:
	$(DC_CMD) build

PHONY += test
test: clean build
	$(DC_CMD) up test_webApp && \
	$(DC_CMD) up test_python && \
	$(MAKE) up

PHONY += down
down:
	$(DC_CMD) down --remove-orphans

PHONY += clean
clean: down
	$(DC_CMD) down --rmi local --volumes
	rm -rf ./static
	rm -rf ./src/javascript/projectQ/applications/web/node_modules

PHONY += help
help:
	@echo -e "Makefile for ProjectQ"
	@echo -e ""
	@echo -e "default:        -> up"
	@echo -e "up:             Start local development stack."
	@echo -e "julia_up:       start local development stack using the julia simulator."
	@echo -e "build:          Builds the docker images for the project."
	@echo -e "test:           -> down build\n" \
	          "               Runs all test, then starts the project for manual\n" \
	          "               testing."
	@echo -e "down:           Stop all containers and removes them."
	@echo -e "clean:          -> down\n" \
	          "               Removes local images and volumes. Purges npm\n" \
	          "               packages. Cleanes up generated files from the\n" \
	          "               web-app and the generated result images.\n" \
	          "               Basically resets the project to \"factory new\"."

.DEFAULT:
	@echo "Target not found:" $@
	@echo "Run 'make help' to view available targets."

.PHONY: $(PHONY)

