import React from 'react';
import PropTypes from 'prop-types';
import { withTranslation } from 'react-i18next';
import { connect } from 'react-redux'

import * as CustomPropTypes from '../customPropTypes.js';
import { toggleExpandSimulation } from '../redux/actionCreators.js';
import { CenterLayout, ContainerLayout } from '../Layouts.jsx';
import ListItem from './ListItem.jsx';


const List = withTranslation()( ({ simulations, toggleExpandSimulation, t }) => {
  let scheduledSimulations = [];
  let finishedSimulations = [];
  simulations.map( simulation => {
    let listItem = (
      <ListItem key={ simulation.id }
        simulation={ simulation }
        onClick={ () => toggleExpandSimulation( simulation.id ) } />
    );

    if ( simulation.finished_at === null ) {
      scheduledSimulations.push( listItem )
    } else {
      finishedSimulations.push( listItem )
    }
  });

  return (
    <ContainerLayout>
      <h2>{ t( 'simulation.list.scheduled' ) }</h2>

      { scheduledSimulations.length > 0 ? (
        <div id="scheduled-simulations" className="mb-5">
          { scheduledSimulations }
        </div>
      ) : (
        <div className="card mb-5">
          <div className="card-body">
            { t( 'simulation.list.emptyScheduled' ) }
          </div>
        </div>
      )}

      <h2>{ t( 'simulation.list.finished' ) }</h2>

      { finishedSimulations.length > 0 ? (
        <div id="finished-simulations" className="mb-5">
          { finishedSimulations }
        </div>
      ) : (
        <div className="card mb-5">
          <div className="card-body">
            { t( 'simulation.list.emptyFinished' ) }
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

