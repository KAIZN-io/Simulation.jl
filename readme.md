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
FLASK_ENV=developent

# exchange names
EXCHANGE_EVENTS=exchange.events

# service names
SERVICE_SIMULATOR=service.simulator
SERVICE_PERSISTOR=service.persistor
```
### Starting

#### Starting the project
To start the project, you just need to:

- Open a terminal in the root of the project
- Run `docker-compose up server`
- Wait for everything to be up and running
- Open your browser and go to: [localhost:8080](http://localhost:8080/)

#### Starting the old python simulation worker
To start the project with the old simulation worker, do the following:

- Open a terminal in the root of the project.
- Run `docker-compose up -d bundler persistor py_simulator`
- Run `docker-compose up --no-deps server`
- Wait for everything to be up and running
- Open your browser and go to: [localhost:8080](http://localhost:8080/)

### Development

#### Develop the Web-App
- Have [npm](https://www.npmjs.com/get-npm) installed
- Open a terminal in the same location and run `docker-compose up server`
- After the project is running, open **another** terminal in the projects root directory
- Change into the web apps code directory by running `cd ./src/javascript/projectQ/applications/web`
- Start the development server with `npm run dev:serve`
- Open your browser and go to: [localhost:808**1**](http://localhost:8081/)

This will automatically rebuild the code for the Web-App on changes and even hot-swap changed components and reload your browser automatically.

#### Running tests
To run the unit tests for the web app, execute: `docker-compose up test_webApp`; To run them locally run `npm run test` in the web apps root dir.
To run the unit tests for the python code, execute: `docker-compose up test_python`; To run them locally run `python -m unittest discover projectQ` in the python root dir.

### Using `make`
The project contains a make file that offers some targets for easier interaction with the project. Run `make help` to see which actions are supported.

### Package management

#### Python
All python dependencies are found in the `requirements.txt` file. You can add, remove or update packages there by editing the file manually.

#### JavaScript
Our web app uses node packages. Management is done with `npm` or compatible node package managers.

#### Julia
In the root of the Julia package we have the `Project.toml` and `Manifest.toml` files. These contain the package definitions for Julia. This allwos us to manage packages with Julias built-in package manager. This is how you manage packages with it:

- Open a terminal in the root of the project
- Run `julia`
- type `]` (closing square bracket)
- run `activate .`
- use `add <PackageName>` to add a new package
- use `rm <PackageName>` to remove a package
- use `up <PackageName>` to update a package to a newer version

All your modifications to the packages will be reflected in the `Project.toml` and `Manifest.toml` respectively.

## Perspective
This software should be the core for the construction of *Design of Experiment* (DoE)

