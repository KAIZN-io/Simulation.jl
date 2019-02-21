import React from 'react';
import PropTypes from 'prop-types';
import { withTranslation } from 'react-i18next';
import withStyles from 'react-jss'
import c from 'classnames/bind';
import moment from 'moment';

import { typeColorMapping } from '../values.js';
import * as CustomPropTypes from '../customPropTypes.js';


const ListItem = withStyles({
  typeBadge: {
    fontFamily: 'Share Tech Mono',
    textTransform: 'uppercase'
  },
  cardHeader: {
    cursor: 'pointer'
  }
})( withTranslation()( ({ simulation, onClick, classes, t }) => {
  let createdAt = moment.utc( simulation.created_at )

  let duration;
  if ( simulation.finished_at ) {
    let startedAt = moment.utc( simulation.started_at );
    let finishedAt = moment.utc( simulation.finished_at );
    duration = moment.duration( finishedAt.diff( startedAt ) );
  }

  return (
    <div className={ c( "card", simulation.expanded ? 'expanded' : 'collapsed' ) } onClick={ onClick }>
      <div className={ c(
        "card-header simulation-card-header d-flex align-items-stretch justify-content-between",
        classes.cardHeader )
      }>

      <div className="d-flex align-items-stretch">
        <span
          className={ c(
            'badge d-inline-flex align-items-center mr-2 pt-1',
            `badge-${ typeColorMapping[ simulation.type ] }`,
            classes.typeBadge
          ) }>
          { simulation.type.substring( 0, 3 ) }
        </span>
        { simulation.name }
      </div>

      <div className="small text-secondary" title={ createdAt.format("DD.MM.YYYY HH:mm:ss") }>
        { createdAt.fromNow() }
      </div>

    </div>

    { simulation.expanded && (
      <div className="card-body">

        <table className="table mb-0">
          <tbody>
            <tr>
              <th scope="row">{ t( 'simulation.list.timeRange' ) }</th>
              <td>{ simulation.start }s - { simulation.stop }s</td>
            </tr>
            <tr>
              <th scope="row">{ t( 'simulation.list.stepSize' ) }</th>
              <td>{ simulation.step_size }s</td>
            </tr>
            <tr>
              <th scope="row">{ t( 'simulation.list.duration' ) }</th>
              { simulation.finished_at ? (
                <td><span title={ duration.as( 's' ) + 's' }>{ duration.humanize() }</span></td>
              ) : (
                <td>-</td>
              )}
            </tr>
          </tbody>
        </table>

        { simulation.finished_at && (
          <a href={ `/static/images/${ simulation.image_path }` } target="_blank">
            <img className="img-fluid mt-4" src={ `/static/images/${ simulation.image_path }` } />
          </a>
        )}

      </div>
    )}

  </div>
  )
}));
ListItem.propTypes = {
  simulation: CustomPropTypes.simulation.isRequired,
  expanded: PropTypes.bool
};

export default ListItem

