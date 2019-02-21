import { combineReducers } from 'redux'

import * as types from './actionTypes.js'


function simulations( state = {}, action ) {
  switch (action.type) {

    case types.INITIALIZE: {
      let additionalSimulations = {};
      for ( let simulation of action.payload.simulations ) {
        additionalSimulations[ simulation.id ] = { ...simulation, expanded: false };
      }
      return Object.assign({}, state, additionalSimulations );
    }

    case types.TOGGLE_EXPAND_SIMULATION: {
      let combined = Object.assign( {}, state[ action.payload.id ], { expanded: !state[ action.payload.id ].expanded } );
      let updatedSimulation ={};
      updatedSimulation[ action.payload.id ] = combined;
      return Object.assign({}, state, updatedSimulation );
    }

    case types.ADD_SCHEDULED_SIMULATION: {
      let newSimulation ={};
      newSimulation[ action.payload.id ] = action.payload;
      return Object.assign({}, state, newSimulation );
    }

    case types.MARK_SIMULATION_AS_STARTED: {
      let combined = Object.assign( {}, state[ action.payload.id ], action.payload );
      let updatedSimulation ={};
      updatedSimulation[ action.payload.id ] = combined;
      return Object.assign({}, state, updatedSimulation );
    }

    case types.MARK_SIMULATION_AS_FINISHED: {
      let combined = Object.assign( {}, state[ action.payload.id ], action.payload );
      let updatedSimulation ={};
      updatedSimulation[ action.payload.id ] = combined;
      return Object.assign({}, state, updatedSimulation );
    }

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

