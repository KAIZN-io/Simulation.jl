import React from 'react';
import ReactDOM from 'react-dom';
import withStyles from 'react-jss';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';

import './init.js';
import store from './redux/store.js';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import Home from './components/Home.jsx';
import SimulationRouter from './components/simulation/Router.jsx';


// Define our root component
// It serves as a router and adds basic layout Components
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

// Render the root component to the actual DOM
// We wrap the component in our redux store provider as well as our routing provider.
// This way we can work with routing and our state in all other components
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

// If the app is served from the webpack dev server, we can enable hot reloading
if( DEV_SERVER ) {
  module.hot.accept();
}

