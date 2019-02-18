# Bachelor Thesis - Software
This repository enables you to simulate the hog, ion, volume and combined model presented in my thesis.

**annotation:** This software is only in a beta-version. The whole used analysis of the models is not implemented yet
but the code is accessible.
	
## Usage

### Requirements
- Download and install [docker](https://hub.docker.com/search/?type=edition&offering=community).
- Download and install [npm](https://www.npmjs.com/get-npm).

### Normal start

**Disclaimer** This will start the project so you can view and interact with it in your browser. This will **not**
start the Web-App in development mode. Changes to the Web-App will require a manual rebuild of its code.
If you want to develop the Web-App, please see 'Develop the Web-App'.

Normal startup routine:
- Open a terminal in the root of the project.
- Run `npm run build`
- Run `docker-compose up`
- Wait for everything to be up and running
- Open your browser and go to: [localhost:8080](http://localhost:8080/)

### Develop the Web-App
- Open a terminal in the same location and run `docker-compose up`
- Open **another** terminal in the root of the project and run `npm run dev`
- Wait for everything to be up and running
- Open your browser and go to: [localhost:808**1**](http://localhost:8081/)

This will automatically rebuild the code for the Web-App on changes and even hot-swap changed components.

## Perspective
This software should be the core for the construction of *Design of Experiment* (DoE)

