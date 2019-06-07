import * as types from './actionTypes.js'


export function initialize( simulations ) {
  return {
    type: types.INITIALIZE,
    payload: {
      simulations: simulations
    }
  };
}

export function toggleExpandNavbar( simulationId ) {
  return {
    type: types.TOGGLE_EXPAND_NAVBAR,
  };
}

export function toggleExpandSimulation( simulationId ) {
  return {
    type: types.TOGGLE_EXPAND_SIMULATION,
    payload: {
      id: simulationId
    }
  };
}

export function addScheduledSimulation( simulation ) {
  return {
    type: types.ADD_SCHEDULED_SIMULATION,
    payload: simulation
  };
}

export function markSimulationAsStarted( updatedData ) {
  return {
    type: types.MARK_SIMULATION_AS_STARTED,
    payload: updatedData
  };
}

export function markSimulationAsFinished( updatedData ) {
  return {
    type: types.MARK_SIMULATION_AS_FINISHED,
    payload: updatedData
  };
}

export function markSimulationAsFailed( updatedData ) {
  return {
    type: types.MARK_SIMULATION_AS_FAILED,
    payload: updatedData
  };
}

