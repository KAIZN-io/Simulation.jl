import io from 'socket.io-client';

import store from './redux/store.js';
import * as actions from './redux/actionCreators.js';


const socket = io('http://localhost:8080/');

socket.on('simulation.scheduled', data => {
  store.dispatch( actions.addScheduledSimulation( data ) );
});

socket.on('simulation.started', data => {
  store.dispatch( actions.markSimulationAsStarted( data ) );
});

socket.on('simulation.finished', data => {
  store.dispatch( actions.markSimulationAsFinished( data ) );
});

