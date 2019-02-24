import React from 'react';
import { Route, Switch } from 'react-router-dom'

import List from './List.jsx'
import New from './New.jsx'


class Simulation extends React.PureComponent {
  render() {
    let { match } = this.props
    return (
      <Switch>
        <Route path={ match.url + '/list' } component={ List } />
        <Route path={ match.url + '/new' } component={ New } />
      </Switch>
    );
  }
}

export default Simulation;

