import React from 'react';
import { Link, NavLink } from 'react-router-dom'
import { withTranslation } from 'react-i18next';
import c from 'classnames/bind';
import { connect } from 'react-redux';

import { toggleExpandNavbar } from '../redux/actionCreators.js';


const Navbar = withTranslation()( ({ expanded, toggleExpandNavbar, t }) => (
  <nav className="navbar navbar-expand-sm navbar-light bg-light">

    <Link className="navbar-brand" to="/app">
      { t('title') }
    </Link>

    <button className="navbar-toggler" type="button" onClick={ toggleExpandNavbar }>
      <i className="fas fa-bars"></i>
    </button>

    <div className={ c( "navbar-collapse", { "collapse": !expanded } ) }>
      <ul className="navbar-nav mr-auto">

        <li className="nav-item">
          <NavLink activeClassName="active" className="nav-link" to="/app/simulation/new">
            <i className="fas fa-plus"></i> {t('navbar.new-simulation')}
          </NavLink>
        </li>

        <li className="nav-item">
          <NavLink activeClassName="active" className="nav-link" to="/app/simulation/list">
            { t('navbar.simulation-overview') }
          </NavLink>
        </li>

      </ul>
    </div>

  </nav>
));

const ConnectedNavbar = connect(
  state => {
    return {
      expanded: state.navbar.expanded,
    }
  },
  dispatch => {
    return {
      toggleExpandNavbar: () => {
        dispatch( toggleExpandNavbar() )
      }
    }
  },
)( Navbar )

export default ConnectedNavbar;

