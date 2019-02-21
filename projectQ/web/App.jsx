import React from 'react';
import ReactDOM from 'react-dom';
import withStyles from 'react-jss'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import io from 'socket.io-client';
import WebFont from 'webfontloader';
import moment from 'moment';

import i18n from './i18n.js';
import Navbar from './Navbar.jsx'
import Footer from './Footer.jsx'
import Home from './Home.jsx'
import SimulationRouter from './Simulation/Router.jsx'


WebFont.load({
  google: {
    families: ['Share Tech Mono', 'Noto Sans'],
  }
});

const socket = io('http://localhost:8080/');
socket.on('connect', function(){
  console.log('connected!')
});
socket.on('simulation.finished', data => {
  console.log( data )
})

moment.updateLocale('en', {
    relativeTime: i18n.t( 'misc:relativeTime', { returnObjects: true })
});

const appStyles = {
  '@global': {
    body: {
      fontFamily: "'Noto Sans', sans-serif",
      color: '#0b0020',
    },
  },
}

class _App extends React.Component {
  render() {
    let { t, classes } = this.props;
    return (
      <>
        <Navbar />
        <Switch>
          <Route exact path="/app" component={ Home } />
          <Route path="/app/simulation" component={ SimulationRouter } />
        </Switch>
        <Footer />
      </>
    );
  }
}
const App = withStyles( appStyles )( _App )

ReactDOM.render(
  (
    <BrowserRouter>
      <App />
    </BrowserRouter>
  ),
  document.getElementById('react-root')
);

module.hot.accept();

