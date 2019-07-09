import PropTypes from 'prop-types';


export const simulation = PropTypes.shape({
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

  expanded: PropTypes.bool,
});

