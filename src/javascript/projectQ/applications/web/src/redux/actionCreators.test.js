import * as types from './actionTypes.js'
import * as actions from './actionCreators.js'


describe('actions', () => {
  it('should create an action to initialize', () => {
    const simulations = [
      {
        id: 1,
      }
    ]
    const expectedAction = {
      type: types.INITIALIZE,
      payload: {
        simulations: [
          {
            id: 1
          }
        ]
      }
    }
    expect( actions.initialize( simulations ) ).toEqual( expectedAction )
  })
})

