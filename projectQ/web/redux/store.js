import { createStore } from 'redux';

import reducer from './reducers';


// Create our store with the reducers we defined
const store = createStore( reducer );
export default store;

