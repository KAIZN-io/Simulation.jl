import io from 'socket.io-client';

import store from './redux/store.js';
import * as actions from './redux/actionCreators.js';
import { HOST } from './values.js';


// define the sockets options
// When being served from the dev server, only use polling
let options = DEV_SERVER ? {
  transports: ['polling']
} : {};

// create the socket
const socket = io( HOST, options );

// define listener
// We just map the socket events to changes in our apps state (redux store)
// You would probably don't need to do anything else with these socket events
socket.on('simulation.scheduled', event => {
  store.dispatch( actions.addScheduledSimulation( event.payload ) );
});

socket.on('simulation.started', event => {
  store.dispatch( actions.markSimulationAsStarted( event.payload ) );
});

socket.on('simulation.finished', event => {
  store.dispatch( actions.markSimulationAsFinished( event.payload ) );
});

socket.on('simulation.failed', event => {
  store.dispatch( actions.markSimulationAsFailed( event.payload ) );
});

