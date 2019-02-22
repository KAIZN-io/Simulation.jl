import { combineReducers } from 'redux';
import moment from 'moment';
import { OrderedMap, Map } from 'immutable';

import * as types from './actionTypes.js';


function initializeSimulation( simulation ) {
  return new Map({
    ...simulation,
    created_at: simulation.created_at ? moment.utc( simulation.created_at ) : null,
    started_at: simulation.started_at ? moment.utc( simulation.started_at ) : null,
    finished_at: simulation.finished_at ? moment.utc( simulation.finished_at ) : null,
    expanded: false,
  });
}

function simulations( state = new OrderedMap(), action ) {
  switch (action.type) {

    case types.INITIALIZE: {
      let additionalSimulations = {};
      for ( let simulation of action.payload.simulations ) {
        additionalSimulations[ simulation.id ] = initializeSimulation( simulation )
      }
      return state.merge( additionalSimulations );
    }

    case types.TOGGLE_EXPAND_SIMULATION:
      return state.update(
        `${ action.payload.id }`,
        simulation => simulation.update( 'expanded', expanded => !expanded )
      );

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

function initialized( state = false, action ) {
  switch (action.type) {

    case types.INITIALIZE: {
      return true
    }

    default:
      return state
  }
}

const reduce = combineReducers({
  simulations,
  initialized
})

export { reduce as default }

