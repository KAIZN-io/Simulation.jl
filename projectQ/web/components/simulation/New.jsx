import React from 'react';
import { withTranslation } from 'react-i18next';

import { ContainerLayout } from '../Layouts.jsx';


const New = withTranslation()( ({ t }) => (
  <ContainerLayout>
    { t( 'simulation.form.wipMessage' ) }
  </ContainerLayout>
));

export default New;

