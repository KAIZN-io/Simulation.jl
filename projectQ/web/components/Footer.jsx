import React from 'react';
import { withTranslation } from 'react-i18next';


class Footer extends React.PureComponent {
  render() {
    let { t, classes } = this.props;
    return (
      <div className="footer container-fluid mt-5 bg-light">
        <div className="container">
          <div className="row">
            <div className="col-12 py-3">
              <small>
                {t('title')} - <i className="far fa-copyright"></i> {t('footer.copyright')}
              </small>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default withTranslation()( Footer );

