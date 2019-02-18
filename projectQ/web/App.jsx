import React from 'react';
import ReactDOM from 'react-dom';
import injectSheet from 'react-jss';
import { withTranslation } from 'react-i18next';
import moment from  'moment';
import WebFont from 'webfontloader';

import './i18n';


// WebFont.load({
//   google: {
//     families: ['Noto Sans', 'Noto Serif'],
//   }
// });


const styles = {
}

class _App extends React.PureComponent {
  render() {
    let { t, classes } = this.props;
    return (
      <div>
        <h1>
          {t('title')}
        </h1>
      </div>
    );
  }
}
const App = withTranslation()( injectSheet( styles )( _App ) );


ReactDOM.render(
  <App />,
  document.getElementById('react-root')
);

module.hot.accept();

