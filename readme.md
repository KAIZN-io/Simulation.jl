# Bachelor Thesis - Software
This repository enables you to simulate the hog, ion, volume and combined model presented in my thesis.

**annotation:** This software is only in a beta-version. The whole used analysis of the models is not implemented yet
but the code is accessible.

## Usage

### Requirements
- Download and install [docker](https://hub.docker.com/search/?type=edition&offering=community).
- Have an `.env` file placed in the projects root, it must look something like this:
```
### General ###
# Debug option for more detailed logging and code reloading in Flask
# 1 = enabled, 0 = disabled
DEBUG=0

### Database Settings ###
# Name of the database
DB_NAME=simulation_results
# Postgres username
DB_USER=postgres
# Postgres password
DB_PASSWORD=password

# Web settings
FLASK_ENV=develompent

# exchange names
EXCHANGE_EVENTS=events

# service names
SERVICE_SIMULATION_WORKER=service.simulation-worker
SERVICE_DB_WORKER=service.db-worker

```

### Starting the project
To start the project, you just need to:
- Open a terminal in the root of the project.
- Run `docker-compose up server`
- Wait for everything to be up and running
- Open your browser and go to: [localhost:8080](http://localhost:8080/)

### Starting the old python simulation worker
To start the project with the old simulation worker, do the following:
- Open a terminal in the root of the project.
- Run `docker-compose up -d bundler dbWorker py_simulation`
- Run `docker-compose up --no-deps server`
- Wait for everything to be up and running
- Open your browser and go to: [localhost:8080](http://localhost:8080/)

### Develop the Web-App
- Have [npm](https://www.npmjs.com/get-npm) installed
- Open a terminal in the same location and run `docker-compose up server`
- After the project is running, open **another** terminal in the root of the project and run `npm run dev-server`
- Open your browser and go to: [localhost:808**1**](http://localhost:8081/)

### Running tests
To run the unit tests for the web app, execute: `docker-compose up test_webApp`; To run them locally: `npm run test`
To run the unit tests for the python code, execute: `docker-compose up test_python`; To run them locally: `python -m unittest discover projectQ`

### Using `make`
The project contains a make file that offers some targets for easier interaction with the project. Run `make help` to see which actions are supported.

This will automatically rebuild the code for the Web-App on changes and even hot-swap changed components and reload your browser automatically.

## Perspective
This software should be the core for the construction of *Design of Experiment* (DoE)

