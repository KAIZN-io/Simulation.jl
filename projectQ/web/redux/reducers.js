import { combineReducers } from 'redux';
import moment from 'moment';
import { OrderedMap, Map } from 'immutable';

import * as types from './actionTypes.js';


/**
 * Initialize simulation data
 *
 * This function takes a simulation that was either acquired from the servers api
 * or pushed via the websocket. These simulations were in JSON format, so all values
 * are strings. This function takes some of these strings and transforms them into
 * object. This way it is easier to work with the simulation and its values.
 * It also adds fields that are needed for the web app only and are not stored - or
 * shouldn't even be stored - in the database.
 */
function initializeSimulation( simulation ) {
  return new Map({
    ...simulation,
    created_at: simulation.created_at ? moment.utc( simulation.created_at ) : null,
    started_at: simulation.started_at ? moment.utc( simulation.started_at ) : null,
    finished_at: simulation.finished_at ? moment.utc( simulation.finished_at ) : null,
    expanded: false,
  });
}

/**
 * Simulations reducer
 *
 * This reducer cares about the `simulations` part of the state.
 * It updates the simulations whenever changes from the server get pushed with the websocket.
 */
function simulations( state = new OrderedMap(), action ) {
  switch (action.type) {

    // Add current set of simulations to the state.
    // This set was just fetched from the servers api
    case types.INITIALIZE: {
      let additionalSimulations = {};
      for ( let simulation of action.payload.simulations ) {
        additionalSimulations[ simulation.id ] = initializeSimulation( simulation )
      }
      return state.merge( additionalSimulations );
    }

    // Expand the simulation in the overview, exposing or hiding its details
    case types.TOGGLE_EXPAND_SIMULATION:
      return state.update(
        `${ action.payload.id }`,
        simulation => simulation.update( 'expanded', expanded => !expanded )
      );

    // Adds a newly scheduled simulation to the list of simulations
    case types.ADD_SCHEDULED_SIMULATION:
      return state.set(
        `${ action.payload.id }`,
        initializeSimulation( action.payload )
      );

    case types.MARK_SIMULATION_AS_STARTED:
      return state.update(
        `${ action.payload.id }`,
        simulation => simulation.set( 'started_at', moment.utc( action.payload.started_at ) )
      );

    case types.MARK_SIMULATION_AS_FINISHED:
      return state.update(
        `${ action.payload.id }`,
        simulation => simulation.withMutations( simulation =>
          simulation
            .set( 'finished_at', moment.utc( action.payload.finished_at ) )
            .set( 'image_path', action.payload.image_path )
        )
      );

    default:
      return state
  }
}

/**
 * Initialized reducer
 *
 * this reducer cares about the `initialized` flag in our state.
 * It is pretty simple, once the `INITIALIZE` action accurs, it just sets the flag to `true`.
 */
function initialized( state = false, action ) {
  switch (action.type) {

    case types.INITIALIZE: {
      return true
    }

    default:
      return state
  }
}

// Combine multiple functions into one reducer
// The functions will only handle the part of the state that they are named after
const reduce = combineReducers({
  simulations,
  initialized
})

export default reduce

