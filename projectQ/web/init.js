import WebFont from 'webfontloader';
import moment from 'moment';

import i18n from './i18n.js';
import './socket.js';
import store from './redux/store.js';
import { initialize } from './redux/actionCreators.js';
import { HOST } from './values.js';


fetch( HOST + '/api/simulation/list')
  .then( response => response.json() )
  .then( jsonData => {
    store.dispatch( initialize( jsonData ) )
  })
  .catch( error => {
    console.error( error )
  });

WebFont.load({
  google: {
    families: ['Share Tech Mono', 'Noto Sans'],
  }
});

moment.updateLocale('en', {
    relativeTime: i18n.t( 'misc:relativeTime', { returnObjects: true })
});

