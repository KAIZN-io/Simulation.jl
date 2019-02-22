import React from 'react';
import PropTypes from 'prop-types';
import { withTranslation } from 'react-i18next';
import { connect } from 'react-redux'

import * as CustomPropTypes from '../../customPropTypes.js';
import { toggleExpandSimulation } from '../../redux/actionCreators.js';
import { CenterLayout, ContainerLayout } from '../Layouts.jsx';
import ListItem from './ListItem.jsx';


const List = withTranslation()( ({ simulations, toggleExpandSimulation, t }) => {
  let simulationList = simulations.map( simulation => {
    return (
      <ListItem key={ simulation.id }
        simulation={ simulation }
        onClick={ () => toggleExpandSimulation( simulation.id ) } />
    );
  });

  return (
    <ContainerLayout>
      <h2>{ t( 'simulation.list.overview' ) }</h2>

      { simulationList.length > 0 ? (
        <div className="accordion mb-5">
          { simulationList }
        </div>
      ) : (
        <div className="card mb-5">
          <div className="card-body">
            { t( 'simulation.list.empty' ) }
          </div>
        </div>
      )}
    </ContainerLayout>
  )
});
List.propTypes = {
  simulations: PropTypes.arrayOf( CustomPropTypes.simulation.isRequired )
};

const ConnectedList = connect(
  state => {
    return {
      simulations: Object.values( state.simulations )
    }
  },
  dispatch => {
    return {
      toggleExpandSimulation: id => {
        dispatch( toggleExpandSimulation( id ) )
      }
    }
  },
)( List )


const ListLoader = withTranslation()( ({ initialized, t }) => {
  return (
    initialized ? (
      <ConnectedList />
    ) : (
      <CenterLayout>
        <div className="spinner-border text-primary mb-3"></div>
        <h3 className="text-secondary">
          { t( 'simulation.list.loading' ) }
        </h3>
      </CenterLayout>
    )
  );
});

const ConnectedListLoader = connect(
  state => {
    return {
      initialized: state.initialized
    }
  }
)( ListLoader )

export default ConnectedListLoader

