import io from 'socket.io-client';

import store from './redux/store.js';
import * as actions from './redux/actionCreators.js';


const socket = io('http://localhost:8080/');

socket.on('simulation.scheduled', event => {
  store.dispatch( actions.addScheduledSimulation( event.payload ) );
});

socket.on('simulation.started', event => {
  store.dispatch( actions.markSimulationAsStarted( event.payload ) );
});

socket.on('simulation.finished', event => {
  store.dispatch( actions.markSimulationAsFinished( event.payload ) );
});

