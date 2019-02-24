import WebFont from 'webfontloader';
import moment from 'moment';

import i18n from './i18n.js';
import './socket.js';
import store from './redux/store.js';
import { initialize } from './redux/actionCreators.js';
import { HOST } from './values.js';


// some console output just for seeing what is going on
console.log( 'Running in ' + MODE + ' mode.');
console.log( 'Served from webpack dev server: ' + DEV_SERVER );
console.log( 'Using host name: ' + HOST );

// get the current list of simulations from the server
fetch( HOST + '/api/simulation/list')
  .then( response => response.json() )
  .then( jsonData => {
    // store simulations in the redux store
    store.dispatch( initialize( jsonData ) )
  })
  .catch( error => {
    console.error( error )
  });

// Load the necessary web fonts
WebFont.load({
  google: {
    families: ['Share Tech Mono', 'Noto Sans'],
  }
});

// set the humanized time spans as defined in our localization files
moment.updateLocale('en', {
    relativeTime: i18n.t( 'misc:relativeTime', { returnObjects: true })
});

