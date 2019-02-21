import * as types from './actionTypes.js'
import reducer from './reducers.js'


describe('reducer', () => {
  it('should return the initial state', () => {
    expect(reducer(undefined, {})).toEqual({
      initialized: false,
      simulations: {}
    })
  })

  it('should handle INITIALIZE', () => {
    let state = reducer(undefined, {});
    let action = {
      type: types.INITIALIZE,
      payload: {
        simulations: [
          {
            id: 1
          },
          {
            id: 2
          }
        ]
      }
    };
    let nextState = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
          expanded: false
        },
        2: {
          id: 2,
          expanded: false
        }
      }
    }
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle TOGGLE_EXPAND_SIMULATION', () => {
    let state = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
          expanded: false
        }
      }
    };
    let action = {
      type: types.TOGGLE_EXPAND_SIMULATION,
      payload: {
        id: 1
      }
    };
    let nextState = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
          expanded: true
        }
      }
    }
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle ADD_SCHEDULED_SIMULATION', () => {
    let state = {
      initialized: true,
      simulations: {
        1: {
          id: 1
        }
      }
    };
    let action = {
      type: types.ADD_SCHEDULED_SIMULATION,
      payload: {
        id: 2,
      }
    };
    let nextState = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
        },
        2: {
          id: 2,
        }
      }
    };
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle MARK_SIMULATION_AS_STARTED', () => {
    let state = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
          started_at: null
        }
      }
    };
    let action = {
      type: types.MARK_SIMULATION_AS_FINISHED,
      payload: {
        id: 1,
        started_at: '2019-02-21T15:21:29-08:00'
      }
    };
    let nextState = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
          started_at: '2019-02-21T15:21:29-08:00'
        }
      }
    };
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle MARK_SIMULATION_AS_FINISHED', () => {
    let state = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
          started_at: '2019-02-21T15:21:29-08:00'
        }
      }
    };
    let action = {
      type: types.MARK_SIMULATION_AS_FINISHED,
      payload: {
        id: 1,
        finished_at: '2019-02-21T15:23:03-08:00'
      }
    };
    let nextState = {
      initialized: true,
      simulations: {
        1: {
          id: 1,
          started_at: '2019-02-21T15:21:29-08:00',
          finished_at: '2019-02-21T15:23:03-08:00'
        }
      }
    };
    expect( reducer( state, action ) ).toEqual( nextState );
  });
});

