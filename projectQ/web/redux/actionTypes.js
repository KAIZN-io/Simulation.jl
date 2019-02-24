/**
 * Here we define the names of the actions that can occur and alter the state of our app
 */

// The initialize action is used once in the beginning to initialize the app with the current set of simulations
export const INITIALIZE = 'initialize';

// These actions are used to update existing simulations
export const ADD_SCHEDULED_SIMULATION = 'add-scheduled-simulation';
export const MARK_SIMULATION_AS_STARTED = 'mark-simulation-as-started';
export const MARK_SIMULATION_AS_FINISHED = 'mark-simulation-as-finished';

// This action toggles the displayment of a simulation in the simulation overview
export const TOGGLE_EXPAND_SIMULATION = 'expand-simulation';

