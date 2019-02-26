import React from 'react';
import PropTypes from 'prop-types';
import { withTranslation } from 'react-i18next';
import withStyles from 'react-jss'
import c from 'classnames/bind';
import moment from 'moment';

import { typeColorMapping } from '../../values.js';
import * as CustomPropTypes from '../../customPropTypes.js';


// TODO: let the status be set by the reducer
const simulationStatus = {
  SCHEDULED: 'scheduled',
  RUNNING: 'running',
  FINISHED: 'finished',
  FAILED: 'failed'
};

function getSimulationStatus( simulation ) {
  let status = simulationStatus.SCHEDULED;

  let started_at = simulation.get( 'started_at' );
  let finished_at = simulation.get( 'finished_at' );
  let failed_at = simulation.get( 'failed_at' );

  if ( started_at ) {
    if ( finished_at ) {
      status = simulationStatus.FINISHED;
    } else if ( failed_at ) {
      status = simulationStatus.FAILED;
    } else {
      status = simulationStatus.RUNNING;
    }
  }

  return status;
}

const ListItem = withStyles({
  typeBadge: {
    fontFamily: 'Share Tech Mono',
    textTransform: 'uppercase'
  },
  cardHeader: {
    cursor: 'pointer'
  },
})( withTranslation()( ({ simulation, onClick, classes, t }) => {
  let status = getSimulationStatus( simulation );
  let color = typeColorMapping[ simulation.get( 'type' ) ];

  let createdAt = moment.utc( simulation.get( 'created_at' ) );

  let duration;
  if ( simulation.get( 'finished_at' ) ) {
    let startedAt = moment.utc( simulation.get( 'started_at' ) );
    let finishedAt = moment.utc( simulation.get( 'finished_at' ) );
    duration = moment.duration( finishedAt.diff( startedAt ) );
  }

  let statusIndicator;
  switch( status ) {
    case simulationStatus.SCHEDULED:
      statusIndicator = <i className="fas fa-calendar-day text-secondary"></i>;
      break;
    case simulationStatus.RUNNING:
      statusIndicator = <span className="spinner-grow spinner-grow-sm text-info" role="status"></span>;
      break;
    case simulationStatus.FINISHED:
      statusIndicator = <i className="fas fa-check text-success"></i>;
      break;
    case simulationStatus.FAILED:
      statusIndicator = <i className="fas fa-times text-danger"></i>;
      break;
  }


  return (
    <div className={ c( "card", simulation.get( 'expanded' ) ? 'expanded' : 'collapsed' ) } onClick={ onClick }>
      <div className={ c(
        "card-header simulation-card-header d-flex justify-content-between",
        classes.cardHeader )
      }>

      <div className="d-flex align-items-baseline">
        <span className={ c(
            'badge align-self-stretch d-inline-flex align-items-center mr-2 pt-1 px-2',
            `badge-${ color }`,
            classes.typeBadge
          ) }>
          { simulation.get( 'type' ).substring( 0, 3 ) }
        </span>

        <h5 className="d-inline mb-0 mr-2">{ simulation.get( 'name' ) }</h5>

        <small className="text-secondary" title={ createdAt.format("DD.MM.YYYY HH:mm:ss") }>
          { t( 'simulation.list.createdAt', { time: createdAt.fromNow() } ) }
        </small>
      </div>

      <div className="d-flex align-items-center" title={ t( `simulation.list.status.${ status }` ) }>
          { statusIndicator }
      </div>
    </div>

    { simulation.get( 'expanded' ) && (
      <div className="card-body">

        <table className="table mb-0">
          <tbody>
            <tr>
              <th scope="row">{ t( 'simulation.list.timeRange' ) }</th>
              <td>{ simulation.get( 'start' ) }s - { simulation.get( 'stop' ) }s</td>
            </tr>
            <tr>
              <th scope="row">{ t( 'simulation.list.stepSize' ) }</th>
              <td>{ simulation.get( 'step_size' ) }s</td>
            </tr>
            <tr>
              <th scope="row">{ t( 'simulation.list.duration' ) }</th>
              { simulation.get( 'finished_at' ) ? (
                <td><span title={ duration.as( 's' ) + 's' }>{ duration.humanize() }</span></td>
              ) : (
                <td>-</td>
              )}
            </tr>
          </tbody>
        </table>

        { simulation.get( 'finished_at' ) && (
          <a href={ `/static/images/${ simulation.get( 'image_path' ) }` } target="_blank">
            <img className="img-fluid mt-4" src={ `/static/images/${ simulation.get( 'image_path' ) }` } />
          </a>
        )}

      </div>
    )}

  </div>
  )
}));
ListItem.propTypes = {
};

export default ListItem

