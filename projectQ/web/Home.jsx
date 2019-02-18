import React from 'react';
import { Link } from 'react-router-dom'
import { withTranslation } from 'react-i18next';


class Home extends React.PureComponent {
  render() {
    let { t, classes } = this.props;
    return (
      <div className="jumbotron jumbotron-fluid">
        <div className="container">

          <h1 className="display-4">
            {t('title')}
          </h1>

          <p className="lead">
            {t('home.lead')}
          </p>

          <hr className="my-4" />

          <p>
            {t('home.try-it')}
          </p>
          <Link className="btn btn-primary btn-lg" to="/app/simulation/new" role="button">
            <i className="fas fa-plus"></i> {t('home.try-it-button')}
          </Link>
        </div>
      </div>
    );
  }
}

export default withTranslation()( Home );

