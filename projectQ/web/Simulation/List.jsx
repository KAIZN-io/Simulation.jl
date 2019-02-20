import React from 'react';
import withStyles from 'react-jss'
import { withTranslation } from 'react-i18next';
import PropTypes from 'prop-types';
import { Set } from 'immutable';
import c from 'classnames/bind';
import moment from 'moment';

import { typeColorMapping } from '../values.js';
import { CenterLayout, ContainerLayout } from '../Layouts.jsx';


const simulationPropShape = PropTypes.shape({
  id: PropTypes.number.isRequired,
  created_at: PropTypes.string.isRequired,

  name: PropTypes.string.isRequired,
  image_path: PropTypes.string,
  started_at: PropTypes.string,
  finished_at: PropTypes.string,

  type: PropTypes.string.isRequired,

  start: PropTypes.number.isRequired,
  stop: PropTypes.number.isRequired,
  step_size: PropTypes.number.isRequired,
  co: PropTypes.string.isRequired,
})

const listItemStyles = {
  typeBadge: {
    fontFamily: 'Share Tech Mono',
    textTransform: 'uppercase'
  },
  cardHeader: {
    cursor: 'pointer'
  }
}

class _ListItem extends React.PureComponent {
  render() {
    let { simulation, expanded, onClick, classes, t } = this.props;
    let createdAt = moment.utc( simulation.created_at )

    let humanizedDuration;
    if ( simulation.finished_at ) {
      let startedAt = moment.utc( simulation.started_at );
      let finishedAt = moment.utc( simulation.finished_at );
      humanizedDuration = moment.duration( finishedAt.diff( startedAt ) ).humanize();
    } else {
      humanizedDuration = '-';
    }

    return (
      <div className={ c( "card", expanded ? 'expanded' : 'collapsed' ) } onClick={ onClick }>
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

          <div className="small text-secondary">
            { createdAt.fromNow() }
          </div>

        </div>

        { expanded && (
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
                  <td>{ humanizedDuration }</td>
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
  }
}
_ListItem.propTypes = {
  simulation: simulationPropShape.isRequired,
  expanded: PropTypes.bool
};
const ListItem = withStyles( listItemStyles )( withTranslation()( _ListItem ) );

class _List extends React.PureComponent {
  constructor( props ) {
    super( props );

    this.state = {
      expanded: Set()
    };
  }
  toggleCollapse( simulationId ) {
    this.setState( ({ expanded }) => ({
      expanded: expanded.has( simulationId ) ? expanded.delete( simulationId ) : expanded.add( simulationId )
    }));
  }
  render() {
    let { simulations, t } = this.props

    let scheduledSimulations = [];
    let finishedSimulations = [];
    simulations.map( simulation => {
      let listItem = (
        <ListItem key={ simulation.id }
          simulation={ simulation }
          expanded={ this.state.expanded.has( simulation.id ) }
          onClick={ () => this.toggleCollapse( simulation.id ) } />
      )

      if ( simulation.finished_at === null ) {
        scheduledSimulations.push( listItem )
      } else {
        finishedSimulations.push( listItem )
      }
    })

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
  }
}
_List.propTypes = {
  simulations: PropTypes.arrayOf( simulationPropShape.isRequired )
};
const List = withTranslation()( _List );

class ListLoader extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      simulations: null
    }
  }
  componentWillMount() {
    fetch('http://localhost:8081/api/simulation/list')
      .then( response => response.json() )
      .then( jsonData => {
        this.setState({ simulations: jsonData });
      })
      .catch( error => {
        console.error( error )
      });
  }
  render() {
    let { t } = this.props
    return (
      this.state.simulations === null ? (
        <CenterLayout>
          <div className="spinner-border text-primary mb-3"></div>
          <h3 className="text-secondary">
            { t( 'simulation.list.loading' ) }
          </h3>
        </CenterLayout>
      ) : (
        <List simulations={ this.state.simulations } />
      )
    );
  }
}

export default withTranslation()( ListLoader );

