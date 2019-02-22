import React from 'react';
import { Link, NavLink } from 'react-router-dom'
import { withTranslation } from 'react-i18next';


class Navbar extends React.Component {
  render() {
    let { t, classes } = this.props;
    return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light">

        <Link className="navbar-brand" to="/app">
          {t('title')}
        </Link>

        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">

            <li className="nav-item">
              <NavLink activeClassName="active" className="nav-link" to="/app/simulation/new">
                <i className="fas fa-plus"></i> {t('navbar.new-simulation')}
              </NavLink>
            </li>

            <li className="nav-item">
              <NavLink activeClassName="active" className="nav-link" to="/app/simulation/list">
                {t('navbar.simulation-overview')}
              </NavLink>
            </li>

          </ul>
        </div>

      </nav>
    );
  }
}

export default withTranslation()( Navbar );

