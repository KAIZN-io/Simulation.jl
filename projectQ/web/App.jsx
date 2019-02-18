import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route } from 'react-router-dom'
import io from 'socket.io-client';

import './i18n';
import Navbar from './Navbar.jsx'
import Footer from './Footer.jsx'
import Home from './Home.jsx'
import Simulation from './Simulation/Simulation.jsx'


const socket = io('http://localhost:8080/');
socket.on('connect', function(){
  console.log('connected!')
});

class App extends React.Component {
  render() {
    let { t, classes } = this.props;
    return (
      <>
        <Navbar />
        <main className="main">
          <Route exact path="/app" component={Home} />
          <div className="container mt-5">
            <Route path="/app/simulation" component={Simulation} />
          </div>
        </main>
        <Footer />
      </>
    );
  }
}

ReactDOM.render(
  (
    <BrowserRouter>
      <App />
    </BrowserRouter>
  ),
  document.getElementById('react-root')
);

module.hot.accept();

