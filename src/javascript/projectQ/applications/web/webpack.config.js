const webpack = require('webpack');

module.exports = (env, options) => {
  return {
    entry: './src/App.jsx',
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: ['babel-loader']
        }
      ]
    },
    resolve: {
      extensions: ['*', '.js', '.jsx']
    },
    output: {
      path: __dirname + '/static',
      publicPath: '/',
      filename: 'bundle.js'
    },
    plugins: [
      new webpack.HotModuleReplacementPlugin(),
      new webpack.DefinePlugin({
        MODE: JSON.stringify( options.mode ),
        DEV_SERVER: options['$0'].includes('webpack-dev-server')
      })
    ],
    devServer: {
      publicPath: 'http://localhost:8081/static/',
      hot: true,
      proxy: {
        '/': 'http://localhost:8080'
      }
    }
  }
};
