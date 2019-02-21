import React from 'react';
import ReactDOM from 'react-dom';
import withStyles from 'react-jss';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';

import './init.js';
import store from './redux/store.js';
import Navbar from './Navbar.jsx';
import Footer from './Footer.jsx';
import Home from './Home.jsx';
import SimulationRouter from './Simulation/Router.jsx';


const App = withStyles({
  '@global': {
    body: {
      fontFamily: "'Noto Sans', sans-serif",
      color: '#0b0020',
    },
  },
})( ({ t, classes }) => {
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
});

ReactDOM.render(
  (
    <Provider store={ store }>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  ),
  document.getElementById('react-root')
);

module.hot.accept();

