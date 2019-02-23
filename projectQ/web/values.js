console.log( 'Running in ' + MODE + ' mode.');
console.log( 'Served from webpack dev server: ' + DEV_SERVER );

export const HOST = window.location.protocol + '//' + window.location.host;
console.log( 'Using host name:' + HOST );

export const typeColorMapping = {
  combined_models: 'primary',
  hog: 'danger',
  ion: 'dark',
  volume: 'success',
}

