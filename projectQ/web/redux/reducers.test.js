import moment from 'moment';
import { OrderedMap, Map } from 'immutable';


import * as types from './actionTypes.js'
import reducer from './reducers.js'


describe( 'reducer', () => {
  it( 'should return the initial state', () => {
    expect( reducer( undefined, {} ) ).toEqual({
      initialized: false,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap()
    })
  })

  it('should handle INITIALIZE', () => {
    let state = reducer(undefined, {});
    let action = {
      type: types.INITIALIZE,
      payload: {
        simulations: [
          {
            id: 1,
            created_at: '2019-02-22T01:17:03-08:00',
            started_at: null,
            finished_at: null,
            failed_at: null,
          },
          {
            id: 2,
            created_at: '2019-02-22T01:17:03-08:00',
            started_at: '2019-02-22T01:17:52-08:00',
            finished_at: '2019-02-22T01:18:05-08:00',
            failed_at: null,
          }
        ]
      }
    };
    let nextState = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          created_at: moment.utc( '2019-02-22T01:17:03-08:00' ),
          started_at: null,
          finished_at: null,
          failed_at: null,
          expanded: false
        }),
        2: new Map({
          id: 2,
          created_at: moment.utc( '2019-02-22T01:17:03-08:00' ),
          started_at: moment.utc( '2019-02-22T01:17:52-08:00' ),
          finished_at: moment.utc( '2019-02-22T01:18:05-08:00' ),
          failed_at: null,
          expanded: false
        })
      })
    }
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle TOGGLE_EXPAND_NAVBAR', () => {
    let state = {
      initialized: true,
      navbar: {
        expanded: true
      },
      simulations: new OrderedMap(),
    };
    let action = {
      type: types.TOGGLE_EXPAND_NAVBAR,
    };
    let nextState = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap()
    }
    expect( reducer( state, action ) ).toEqual( nextState );

    state = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap(),
    };
    nextState = {
      initialized: true,
      navbar: {
        expanded: true
      },
      simulations: new OrderedMap()
    }
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle TOGGLE_EXPAND_SIMULATION', () => {
    let state = {
      initialized: true,
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          expanded: false
        })
      })
    };
    let action = {
      type: types.TOGGLE_EXPAND_SIMULATION,
      payload: {
        id: 1
      }
    };
    let nextState = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          expanded: true
        })
      })
    }
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle ADD_SCHEDULED_SIMULATION', () => {
    let state = {
      initialized: true,
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          created_at: moment.utc( '2019-02-22T01:17:03-08:00' ),
          started_at: moment.utc( '2019-02-22T01:17:52-08:00' ),
          finished_at: moment.utc( '2019-02-22T01:18:05-08:00' ),
          failed_at: null,
          expanded: false
        })
      })
    };
    let action = {
      type: types.ADD_SCHEDULED_SIMULATION,
      payload: {
        id: 2,
        created_at: '2019-02-22T01:17:03-08:00',
        started_at: null,
        finished_at: null,
      }
    };
    let nextState = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          created_at: moment.utc( '2019-02-22T01:17:03-08:00' ),
          started_at: moment.utc( '2019-02-22T01:17:52-08:00' ),
          finished_at: moment.utc( '2019-02-22T01:18:05-08:00' ),
          failed_at: null,
          expanded: false
        }),
        2: new Map({
          id: 2,
          created_at: moment.utc( '2019-02-22T01:17:03-08:00' ),
          started_at: null,
          finished_at: null,
          failed_at: null,
          expanded: false
        })
      })
    };
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle MARK_SIMULATION_AS_STARTED', () => {
    let state = {
      initialized: true,
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          started_at: null,
          finished_at: null,
          failed_at: null,
        })
      })
    };
    let action = {
      type: types.MARK_SIMULATION_AS_STARTED,
      payload: {
        id: 1,
        started_at: '2019-02-21T15:21:29-08:00'
      }
    };
    let nextState = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          started_at: moment.utc( '2019-02-21T15:21:29-08:00' ),
          finished_at: null,
          failed_at: null,
        })
      })
    };
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle MARK_SIMULATION_AS_FINISHED', () => {
    let state = {
      initialized: true,
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          started_at: moment.utc( '2019-02-21T15:21:29-08:00' ),
          finished_at: null,
          failed_at: null,
          image_path: null
        })
      })
    };
    let action = {
      type: types.MARK_SIMULATION_AS_FINISHED,
      payload: {
        id: 1,
        finished_at: '2019-02-21T15:23:03-08:00',
        image_path: 'ion_3.png'
      }
    };
    let nextState = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          started_at: moment.utc( '2019-02-21T15:21:29-08:00' ),
          finished_at: moment.utc( '2019-02-21T15:23:03-08:00' ),
          failed_at: null,
          image_path: 'ion_3.png'
        })
      })
    };
    expect( reducer( state, action ) ).toEqual( nextState );
  });

  it('should handle MARK_SIMULATION_AS_FAILED', () => {
    let state = {
      initialized: true,
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          started_at: moment.utc( '2019-02-21T15:21:29-08:00' ),
          finished_at: null,
          failed_at: null
        })
      })
    };
    let action = {
      type: types.MARK_SIMULATION_AS_FAILED,
      payload: {
        id: 1,
        failed_at: '2019-02-21T15:23:03-08:00',
      }
    };
    let nextState = {
      initialized: true,
      navbar: {
        expanded: false
      },
      simulations: new OrderedMap({
        1: new Map({
          id: 1,
          started_at: moment.utc( '2019-02-21T15:21:29-08:00' ),
          finished_at: null,
          failed_at: moment.utc( '2019-02-21T15:23:03-08:00' ),
        })
      })
    };
    expect( reducer( state, action ) ).toEqual( nextState );
  });
});

