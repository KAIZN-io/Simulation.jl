# Bachelor Thesis - Software
This repository enables you to simulate the hog, ion, volume and combined model presented in my thesis.

**annotation:** This software is only in a beta-version. The whole used analysis of the models is not implemented yet
but the code is accessible.

## Usage

### Requirements
- Download and install [docker](https://hub.docker.com/search/?type=edition&offering=community).

### Starting the project
To start the project, you jsut need to:
- Open a terminal in the root of the project.
- Run `docker-compose up`
- Wait for everything to be up and running
- Open your browser and go to: [localhost:8080](http://localhost:8080/)

### Develop the Web-App
- Have [npm](https://www.npmjs.com/get-npm) installed
- Open a terminal in the same location and run `docker-compose up`
- After the project is running, open **another** terminal in the root of the project and run `npm run dev-server`
- Open your browser and go to: [localhost:808**1**](http://localhost:8081/)

This will automatically rebuild the code for the Web-App on changes and even hot-swap changed components and reload your browser automatically.

## Perspective
This software should be the core for the construction of *Design of Experiment* (DoE)

